import sqlite3
from dotenv import dotenv_values

conf = dotenv_values('.env')
db_url = conf["DATABASE_URL"]

def init():
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT
    username TEXT UNIQUE NOT NULL,
    passhash TEXT NOT NULL);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS messages 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    user INTEGER NOT NULL,
    room TEXT NOT NULL,
    time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user) REFRENCES users (id));""")
    
    conn.commit()
    conn.close()


def save_msg(msg):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO messages VALUES ('{msg}');")
    conn.commit()
    conn.close()


def get_all_msg():
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages;")
    messages = cur.fetchall()
    conn.close()
    return [i[0] for i in messages]