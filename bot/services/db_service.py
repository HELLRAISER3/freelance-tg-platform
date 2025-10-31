import sqlite3
from pathlib import Path

DB_PATH = Path("data/database.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT,
            title TEXT,
            posted_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            role TEXT DEFAULT 'unkwown',
            balance REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int, username: str, role: str = "unknown", balance: float = 0.0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, username, role, balance) VALUES (?, ?, ?, ?)", 
                   (user_id, username, role, balance))
    conn.commit()
    conn.close()
    
def add_project(title: str, link: str, posted_by: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (title, link, posted_by) VALUES (?, ?, ?)",
                   (title, link, posted_by))
    conn.commit()
    conn.close()
    
def get_all_projects():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, link, created_at FROM projects ORDER BY created_at DESC
    """)
    projects = cursor.fetchall()
    conn.close()
    return projects

def delete_project(project_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()