import sqlite3
import matplotlib.pyplot as plt

def generate_mood_graph(username):

    conn = sqlite3.connect("database/mental_health.db")
    cur = conn.cursor()

    cur.execute(
    "SELECT emotion,count(*) FROM moods WHERE user=? GROUP BY emotion",
    (username,)
    )

    data = cur.fetchall()

    emotions = [x[0] for x in data]
    counts = [x[1] for x in data]

    plt.figure()
    plt.bar(emotions,counts)
    plt.title("Mood Analytics")
    plt.savefig("static/mood_graph.png")
