import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

load_dotenv()
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

cursor.execute("SELECT * FROM prompts WHERE id = 1")
print(cursor.fetchone())
conn.close()