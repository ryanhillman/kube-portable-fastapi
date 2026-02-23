import os, time
import psycopg2

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "app")
DB_USER = os.getenv("DB_USER", "app")
DB_PASS = os.getenv("DB_PASS", "app-pass")

def conn():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

while True:
    try:
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
                cur.execute("""
                  UPDATE jobs
                  SET status='processing'
                  WHERE id = (
                    SELECT id FROM jobs
                    WHERE status='queued'
                    ORDER BY id ASC
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                  )
                  RETURNING id;
                """)
                row = cur.fetchone()
                if row:
                    job_id = row[0]
                    # pretend work
                    time.sleep(1)
                    cur.execute("UPDATE jobs SET status='done' WHERE id=%s;", (job_id,))
            c.commit()
    except Exception as e:
        print("worker error:", e)
    time.sleep(1)