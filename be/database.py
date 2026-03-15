import sqlite3
import os

DB_PATH = 'instance/users.db'


def init_db():
    os.makedirs('instance', exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  first_name TEXT NOT NULL,
                  last_name TEXT NOT NULL,
                  role TEXT NOT NULL)''')

    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, first_name, last_name, role) VALUES (?,?,?,?,?)",
                  ('admin', 'admin123', 'Admin', 'System', 'admin'))

    conn.commit()
    conn.close()
    print("База данных инициализирована")


def get_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user


def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, first_name, last_name, role FROM users")
    users = c.fetchall()
    conn.close()
    return users

def create_user(username, password, first_name, last_name, role):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, first_name, last_name, role) VALUES (?,?,?,?,?)",
                  (username, password, first_name, last_name, role))
        conn.commit()
        success = True
    except:
        success = False
    conn.close()
    return success