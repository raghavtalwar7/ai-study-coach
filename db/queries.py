GET_STUDENT = "SELECT student_id, active FROM students WHERE student_id=%s"

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
