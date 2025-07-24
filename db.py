import sqlite3

DATABASE_ADDRESS = './db.sqlite3'

def init():
    conn = sqlite3.connect(DATABASE_ADDRESS)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (context TEXT);")
    conn.commit()
    conn.close()


def save_msg(msg):
    conn = sqlite3.connect(DATABASE_ADDRESS)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO messages VALUES ('{msg}');")
    conn.commit()
    conn.close()


def get_all_msg():
    conn = sqlite3.connect(DATABASE_ADDRESS)
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages;")
    messages = cur.fetchall()
    conn.close()
    return [i[0] for i in messages]