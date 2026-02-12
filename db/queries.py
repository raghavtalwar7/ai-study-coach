GET_STUDENT = "SELECT student_id, active FROM students WHERE student_id=%s"

# ─────────────────────────────────────────────────────────────
# Table Creation (run once during setup)
# ─────────────────────────────────────────────────────────────

CREATE_STUDENT_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS student_logs (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    lab VARCHAR(50) NOT NULL,
    section VARCHAR(50) NOT NULL,
    mode VARCHAR(20) NOT NULL,
    hint_level INTEGER NOT NULL,
    user_input TEXT,
    response TEXT,
    hints_remaining INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_student_logs_student_id ON student_logs(student_id);
CREATE INDEX IF NOT EXISTS idx_student_logs_mode ON student_logs(mode);
"""

INIT_HINT_BALANCE = """
INSERT INTO hint_balance(student_id, remaining_hints)
VALUES (%s, 15)
ON CONFLICT (student_id) DO NOTHING
"""

GET_HINTS_LEFT = """
SELECT remaining_hints FROM hint_balance WHERE student_id=%s
"""

LOCK_HINT_USAGE = """
SELECT max_level_used
FROM hint_usage
WHERE student_id=%s AND lab=%s AND section=%s
FOR UPDATE
"""


ATOMIC_DECREMENT_HINT = """
UPDATE hint_balance
SET remaining_hints = remaining_hints - 1
WHERE student_id=%s AND remaining_hints > 0
RETURNING remaining_hints
"""

GET_MAX_LEVEL = """
SELECT max_level_used FROM hint_usage
WHERE student_id=%s AND lab=%s AND section=%s
"""

UPSERT_LEVEL = """
INSERT INTO hint_usage(student_id, lab, section, max_level_used)
VALUES (%s, %s, %s, %s)
ON CONFLICT (student_id, lab, section)
DO UPDATE SET max_level_used = EXCLUDED.max_level_used
"""

# ─────────────────────────────────────────────────────────────
# Student Interaction Logs
# ─────────────────────────────────────────────────────────────

INSERT_LOG = """
INSERT INTO student_logs(student_id, lab, section, mode, hint_level, user_input, response, hints_remaining)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

GET_STUDENT_LOGS = """
SELECT id, student_id, lab, section, mode, hint_level, user_input, response, hints_remaining, created_at
FROM student_logs
WHERE student_id = %s
ORDER BY created_at DESC
"""

GET_STUDENT_MODE_COUNTS = """
SELECT mode, COUNT(*) as count
FROM student_logs
WHERE student_id = %s
GROUP BY mode
"""

GET_ALL_LOGS = """
SELECT id, student_id, lab, section, mode, hint_level, user_input, response, hints_remaining, created_at
FROM student_logs
ORDER BY created_at DESC
LIMIT %s
"""
