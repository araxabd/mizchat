import sqlite3
from dotenv import dotenv_values

conf = dotenv_values('.env')
db_url = conf["DATABASE_URL"]

def init():
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    passhash TEXT NOT NULL);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS messages 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    user INTEGER NOT NULL,
    room TEXT NOT NULL,
    time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user) REFERENCES users (id));""")

    conn.commit()
    conn.close()


def save_msg(msg, user_id, room):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute("INSERT INTO messages VALUES (?, ?, ?);", (msg, user_id, room))
    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?;", (username, ))
    user = cur.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id, ))
    user = cur.fetchone()
    conn.close()
    return user


def set_user(username, hashed_password):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, passhash) VALUES (?, ?);", (username, hashed_password))
    conn.commit()
    conn.close()


def get_room_messages(room, limit=20):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    cur.execute("""SELECT users.username, messages.text, messages.time 
    FROM messages INNER JOIN users ON messages.user=users.id 
    WHERE messages.room = ? 
    ORDER BY messages.time DESC 
    LIMIT ?;""", (room, limit))
    content = cur.fetchall()
    conn.close()
    return [{'user': msg[0], 'txt': msg[1], 'time': msg[2]} for msg in content]

