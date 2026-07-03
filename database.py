import sqlite3
import pandas as pd

conn = sqlite3.connect("/Users/alisaliao/Documents/media_classifier/labeling.db")
cursor = conn.cursor()

# Wipe everything
cursor.execute("DROP TABLE IF EXISTS prompts")
cursor.execute("DROP TABLE IF EXISTS submissions")
cursor.execute("DROP TABLE IF EXISTS reports")

cursor.execute("""
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    response TEXT,
    votes_diagram INTEGER DEFAULT 0,
    votes_video INTEGER DEFAULT 0,
    votes_audio INTEGER DEFAULT 0,
    votes_text INTEGER DEFAULT 0,
    total_votes INTEGER DEFAULT 0,
    is_finalized BOOLEAN DEFAULT 0,
    is_reported BOOLEAN DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,
    session_id TEXT NOT NULL,
    label TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id)
)
""")

cursor.execute("""
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,
    session_id TEXT NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompts(id)
)
""")

conn.commit()

# Load prompts with both columns
df = pd.read_csv("wildchat_prompts.csv")
df[["prompt", "response"]].rename(columns={"prompt": "text"}).to_sql(
    "prompts", conn, if_exists="append", index=False
)

# Verify
cursor.execute("PRAGMA table_info(prompts)")
for col in cursor.fetchall():
    print(col)
cursor.execute("SELECT COUNT(*) FROM prompts")
print(cursor.fetchone())

conn.close()
print("done")