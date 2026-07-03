import sqlite3
import pandas as pd

conn = sqlite3.connect("labeling.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,
    session_id TEXT NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id)
)
""")

#to see reports
df = pd.read_sql_query("SELECT * FROM prompts WHERE is_reported = 1", conn)
print(df)


conn.commit()
conn.close()