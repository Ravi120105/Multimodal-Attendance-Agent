import sqlite3
from datetime import datetime
from config import DB_PATH, BASE_DIR

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    schema_path = BASE_DIR / "database" / "schema.sql"
    if schema_path.exists():
        with open(schema_path, "r") as f:
            cursor.executescript(f.read())
    conn.commit()
    conn.close()

def create_session(session_id, session_name, course_code):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT OR REPLACE INTO sessions (session_id, session_name, course_code, start_time, status) VALUES (?, ?, ?, ?, 'Active')",
        (session_id, session_name, course_code, now)
    )
    conn.commit()
    conn.close()

def get_active_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions ORDER BY start_time DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def register_participant(participant_id, full_name, enrollment_number):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    try:
        cursor.execute(
            "INSERT INTO participants (participant_id, full_name, enrollment_number, consent_given, registered_at) VALUES (?, ?, ?, 1, ?)",
            (participant_id, full_name, enrollment_number, now)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def get_participants():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM participants")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def log_attendance(session_id, participant_id, status="Present", confidence=1.0):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO attendance_records (session_id, participant_id, timestamp, status, confidence) VALUES (?, ?, ?, ?, ?)",
        (session_id, participant_id, now, status, confidence)
    )
    conn.commit()
    conn.close()

def get_attendance_records(session_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if session_id:
        cursor.execute("""
            SELECT r.*, p.full_name, p.enrollment_number 
            FROM attendance_records r
            JOIN participants p ON r.participant_id = p.participant_id
            WHERE r.session_id = ?
        """, (session_id,))
    else:
        cursor.execute("""
            SELECT r.*, p.full_name, p.enrollment_number 
            FROM attendance_records r
            JOIN participants p ON r.participant_id = p.participant_id
        """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]