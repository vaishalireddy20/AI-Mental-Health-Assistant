import sqlite3

def save_mood(user,message,emotion):

    conn=sqlite3.connect("database/mental_health.db")
    cur=conn.cursor()

    cur.execute(
    "CREATE TABLE IF NOT EXISTS mood_history(user TEXT,message TEXT,emotion TEXT)"
    )

    cur.execute(
    "INSERT INTO mood_history VALUES(?,?,?)",
    (user,message,emotion)
    )

    conn.commit()
    conn.close()
