import sqlite3

def create_db():
    conn = sqlite3.connect("matcher.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            resume_text TEXT,
            jd_text TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_match(score, resume, jd):
    conn = sqlite3.connect("matcher.db")
    c = conn.cursor()
    c.execute("INSERT INTO matches (score, resume_text, jd_text) VALUES (?, ?, ?)", (score, resume, jd))
    conn.commit()
    conn.close()
