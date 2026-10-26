CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    session_name TEXT NOT NULL,
    course_code TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    status TEXT DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS participants (
    participant_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    enrollment_number TEXT UNIQUE NOT NULL,
    consent_given INTEGER DEFAULT 1,
    registered_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    participant_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Late', 'Manual')) DEFAULT 'Present',
    confidence REAL DEFAULT 1.0,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id)
);

CREATE TABLE IF NOT EXISTS session_analytics (
    analytics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    avg_movement REAL,
    audio_activity_level REAL,
    active_count INTEGER,
    engagement_score REAL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);