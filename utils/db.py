import sqlite3
import json
import os

DB = "db/reports.db"

def init_db(db_path=DB):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file TEXT,
        path TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        report_json TEXT
    )""")
    conn.commit()
    conn.close()

def save_report(report, db_path=DB):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO reports (file, path, report_json) VALUES (?, ?, ?)",
              (report["file"], report["path"], json.dumps(report)))
    conn.commit()
    conn.close()

def list_reports(db_path=DB):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT report_json FROM reports ORDER BY id DESC LIMIT 200")
    rows = c.fetchall()
    conn.close()
    return [json.loads(r[0]) for r in rows]
