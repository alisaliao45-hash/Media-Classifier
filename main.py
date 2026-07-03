import psycopg2
import psycopg2.extras
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow your frontend to call this API from a browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later to your actual domain
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn

class LabelSubmission(BaseModel):
    prompt_id: int
    session_id: str
    label: str  # "diagram", "video", "audio", "text"

VOTE_THRESHOLD = 3

@app.get("/next-prompt")
def get_next_prompt(session_id: str):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("""
        SELECT p.id, p.text, p.response
        FROM prompts p
        WHERE p.is_finalized = FALSE
        AND p.id NOT IN (
            SELECT prompt_id FROM submissions WHERE session_id = %s
        )
        ORDER BY RANDOM()
        LIMIT 1
    """, (session_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"done": True}

    return {"done": False, "prompt_id": row["id"], "text": row["text"], "response": row["response"]}

@app.post("/submit-label")
def submit_label(submission: LabelSubmission):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Record the individual submission
    cursor.execute("""
        INSERT INTO submissions (prompt_id, session_id, label)
        VALUES (%s, %s, %s)
    """, (submission.prompt_id, submission.session_id, submission.label))
    
    # Update vote counts on the prompt
    label_column = f"votes_{submission.label}"
    cursor.execute(f"""
        UPDATE prompts
        SET {label_column} = {label_column} + 1,
            total_votes = total_votes + 1
        WHERE id = %s
    """, (submission.prompt_id,))
    
    # Check if it's hit the threshold and finalize
    cursor.execute("""
        UPDATE prompts
        SET is_finalized = TRUE
        WHERE id = %s AND total_votes >= %s
    """, (submission.prompt_id, VOTE_THRESHOLD))
    
    conn.commit()
    conn.close()
    
    return {"success": True}


class ReportSubmission(BaseModel):
    prompt_id: int
    session_id: str
    reason: str = ""

@app.post("/report-prompt")
def report_prompt(report: ReportSubmission):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("""
        INSERT INTO reports (prompt_id, session_id, reason)
        VALUES (%s, %s, %s)
    """, (report.prompt_id, report.session_id, report.reason))

    # Pull it out of rotation immediately so others don't see it
    cursor.execute("""
        UPDATE prompts SET is_finalized = TRUE, is_reported =TRUE WHERE id = %s
    """, (report.prompt_id,))

    conn.commit()
    conn.close()

    return {"success": True}