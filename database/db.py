import sqlite3
from datetime import datetime
import os

def setup_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/face_log.db")
    c = conn.cursor()

    # Optional base fallback table (all-time visitors)
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            face_id TEXT PRIMARY KEY,
            first_seen TEXT
        )
    ''')

    # Global events log table
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            face_id TEXT,
            event_type TEXT,
            timestamp TEXT,
            image_path TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_visitor(face_id):
    now = datetime.now()
    table_name = f"visitors_{now.strftime('%Y_%m_%d')}"  # e.g., visitors_2025_07_09

    conn = sqlite3.connect("database/face_log.db")
    c = conn.cursor()

    # Create today's visitor table if not exists
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            face_id TEXT PRIMARY KEY,
            first_seen TEXT
        )
    ''')
    
    # Insert into today's table
    c.execute(f"INSERT OR IGNORE INTO {table_name} (face_id, first_seen) VALUES (?, ?)",
              (face_id, now.isoformat()))

    # Also insert into global visitors table (optional)
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            face_id TEXT PRIMARY KEY,
            first_seen TEXT
        )
    ''')
    c.execute("INSERT OR IGNORE INTO visitors (face_id, first_seen) VALUES (?, ?)",
              (face_id, now.isoformat()))

    conn.commit()
    conn.close()

def log_event_db(face_id, event_type, image_path):
    conn = sqlite3.connect("database/face_log.db")
    c = conn.cursor()
    c.execute("INSERT INTO events (face_id, event_type, timestamp, image_path) VALUES (?, ?, ?, ?)",
              (face_id, event_type, datetime.now().isoformat(), image_path))
    conn.commit()
    conn.close()
