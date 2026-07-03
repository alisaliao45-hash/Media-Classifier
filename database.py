import psycopg2
import psycopg2.extras
import pandas as pd
import os

conn = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

cursor.execute("DROP TABLE IF EXISTS submissions")
cursor.execute("DROP TABLE IF EXISTS reports")
cursor.execute("DROP TABLE IF EXISTS prompts")

cursor.execute("""
CREATE TABLE prompts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    response TEXT,
    votes_diagram INTEGER DEFAULT 0,
    votes_video INTEGER DEFAULT 0,
    votes_audio INTEGER DEFAULT 0,
    votes_text INTEGER DEFAULT 0,
    total_votes INTEGER DEFAULT 0,
    is_finalized BOOLEAN DEFAULT FALSE,
    is_reported BOOLEAN DEFAULT FALSE
)
""")

cursor.execute("""
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    prompt_id INTEGER NOT NULL REFERENCES prompts(id),
    session_id TEXT NOT NULL,
    label TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    prompt_id INTEGER NOT NULL REFERENCES prompts(id),
    session_id TEXT NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Load prompts
df = pd.read_csv("wildchat_prompts.csv")
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO prompts (text, response) VALUES (%s, %s)",
        (row["prompt"], row["response"])
    )

conn.commit()
conn.close()
print("done")