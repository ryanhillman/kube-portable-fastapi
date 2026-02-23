import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "app")
DB_USER = os.getenv("DB_USER", "app")
DB_PASS = os.getenv("DB_PASS", "app-pass")

def conn():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/readyz")
def readyz():
    try:
        with conn() as c:
            with c.cursor() as cur:
                cur.execute("SELECT 1;")
        return {"ready": True}
    except Exception as e:
        return {"ready": False, "error": str(e)}

@app.post("/jobs")
def enqueue_job(payload: dict):
    """
    Portable queue: write a job row into Postgres.
    Worker will process rows.
    """
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                  id SERIAL PRIMARY KEY,
                  payload JSONB NOT NULL,
                  status TEXT NOT NULL DEFAULT 'queued',
                  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
            """)
            cur.execute("INSERT INTO jobs (payload) VALUES (%s) RETURNING id;", (psycopg2.extras.Json(payload),))
            job_id = cur.fetchone()[0]
        c.commit()
    return {"job_id": job_id, "status": "queued"}

@app.get("/jobs/next")
def next_job():
    with conn() as c:
        with c.cursor() as cur:
            cur.execute("""
              SELECT id, payload, status FROM jobs
              WHERE status='queued'
              ORDER BY id ASC
              LIMIT 1;
            """)
            row = cur.fetchone()
            if not row:
                return {"job": None}
            return {"job": {"id": row[0], "payload": row[1], "status": row[2]}}