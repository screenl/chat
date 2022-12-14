import os.path
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "users.db")

def create_user(username,passwd):
    p = 1
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        t = c.execute(f"SELECT * FROM users WHERE username='{username}'").fetchall()
        if not t:
            c.execute('INSERT INTO users VALUES (?,?)',(username,passwd))
        else:
            print('Username already exists')
            p = 0
        conn.commit()
    return p

def get_password(username):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        t = c.execute(f"SELECT * FROM users WHERE username='{username}'").fetchall()
        if t:
            return t[0][1]
        else:
            return None
def get_users():
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        t = c.execute(f"SELECT username FROM users").fetchall()
        return t[0]

if __name__=='__main__':
    print(get_password('admin'))
    print(get_users())