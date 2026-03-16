from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import random
from textblob import TextBlob

from emotion_model import detect_emotion
from crisis_detection import detect_crisis
from mood_history import save_mood

app = Flask(__name__)
app.secret_key = "mentalhealth"


# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------
def init_db():

    conn = sqlite3.connect("database/mental_health.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mood_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    message TEXT,
    emotion TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


init_db()

def save_mood(username,message,emotion):

    conn=sqlite3.connect("database/mental_health.db")
    cursor=conn.cursor()

    cursor.execute(
    "INSERT INTO mood_history(username,message,emotion) VALUES(?,?,?)",
    (username,message,emotion)
    )

    conn.commit()
    conn.close()
# -----------------------------
# MOOD DETECTION
# -----------------------------
def detect_mood(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0:
        return "Happy"
    elif polarity < 0:
        return "Sad"
    else:
        return "Neutral"


# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route("/")
def login():
    return render_template("login.html")


# -----------------------------
# REGISTER
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        user = request.form["user"]
        password = request.form["password"]

        conn = sqlite3.connect("database/mental_health.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (user, password)
        )

        conn.commit()
        conn.close()

        # store user in session
        session["user"] = user

        return redirect("/chat")

    return render_template("register.html")


# -----------------------------
# DASHBOARD (MOOD ANALYTICS)
# -----------------------------
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database/mental_health.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emotion, COUNT(*) FROM mood_history GROUP BY emotion"
    )

    data = cursor.fetchall()

    conn.close()

    moods = [row[0] for row in data]
    counts = [row[1] for row in data]

    return render_template(
        "dashboard.html",
        moods=moods,
        counts=counts
    )


# -----------------------------
# MOOD ANALYTICS PAGE
# -----------------------------
@app.route("/mood_analytics")
def mood_analytics():

    conn = sqlite3.connect("database/mental_health.db")
    cursor = conn.cursor()

    cursor.execute("SELECT emotion, COUNT(*) FROM mood_history GROUP BY emotion")

    data = cursor.fetchall()

    conn.close()

    moods = [row[0] for row in data]
    counts = [row[1] for row in data]

    return render_template("mood_analytics.html", moods=moods, counts=counts)


# -----------------------------
# CHAT PAGE
# -----------------------------
@app.route("/chat")
def chat():
    return render_template("chat.html")


# -----------------------------
# CHATBOT RESPONSE
# -----------------------------
@app.route("/get_response", methods=["POST"])
def response():

    
    data = request.get_json()

    user_text = data.get("message","").lower()

    print("User message:", user_text)

    emotion = detect_mood(user_text)
    
    # Save mood to database
    save_mood(session.get("user", "guest"), user_text, emotion)

    if detect_crisis(user_text):

        return jsonify({
            "reply":
            "I'm really sorry you're feeling this way.\n\n"
            "Please contact the Mental Health Helpline immediately.\n"
            "☎ 915298721",
            "emotion": emotion
        })

    # SAD RESPONSES
    if "sad" in user_text:

        responses = [
            "I'm really sorry you're feeling sad. I'm here to listen.",
            "It sounds like you're going through a tough time.",
            "I'm here for you. "
        ]

        tips = (
            "\n\nHere are a few things that may help:\n"
            "• Take 5 slow deep breaths\n"
            "• Listen to calming music\n"
            "• Go for a short walk\n"
            "• Talk to someone you trust\n"
            "Would you like a short breathing exercise?"
        )

        reply = random.choice(responses) + tips

    # ANXIETY
    elif "anxious" in user_text or "anxiety" in user_text:

        reply = (
            "Feeling anxious can be overwhelming.\n\n"
            "Try this grounding exercise:\n"
            "1️⃣ Name 5 things you see\n"
            "2️⃣ Touch 4 things around you\n"
            "3️⃣ Listen for 3 sounds\n"
            "4️⃣ Take 2 deep breaths\n"
            "5️⃣ Think of 1 positive thought\n"
            "Would you like a short breathing exercise?"
        )

    # ANGER
    elif "angry" in user_text or "mad" in user_text:

        reply = (
            "It sounds like you're feeling angry.\n\n"
            "Try these calming techniques:\n"
            "• Deep breathing\n"
            "• Short walk\n"
            "• Write your thoughts down\n"
            "Would you like a short breathing exercise?"
        )

    # STRESS
    elif "stress" in user_text or "stressed" in user_text:

        reply = (
            "Stress can feel heavy sometimes.\n\n"
            "Quick relief tips:\n"
            "• Stretch your body\n"
            "• Drink water\n"
            "• Close your eyes for a minute\n"
            "Would you like a short breathing exercise?"
        )

    # HAPPY
    elif "happy" in user_text:

        reply = (
            "That's wonderful to hear! 😊\n\n"
            "What made you feel happy today?"
        )

    # BREATHING EXERCISE
    elif "yes" in user_text:

        reply = (
            "Great! Let's try a breathing exercise.\n\n"
            "Inhale for 4 seconds\n"
            "Hold for 4 seconds\n"
            "Exhale for 6 seconds\n\n"
            "Repeat 5 times."
        )

    else:

        reply = (
            "Thank you for sharing that with me.\n\n"
            "Would you like:\n"
            "• Relaxation tips\n"
            "• Breathing exercises\n"
            "• Stress management"
        )

    return jsonify({"reply": reply, "emotion": emotion})


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
