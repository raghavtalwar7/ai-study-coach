from db.pool import get_conn, release_conn
from db import queries


def fetch_student(student_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(queries.GET_STUDENT, (student_id,))
            return cur.fetchone()
    finally:
        release_conn(conn)


def init_hint_balance(student_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(queries.INIT_HINT_BALANCE, (student_id,))
            conn.commit()
    finally:
        release_conn(conn)


def get_hints_left(student_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(queries.GET_HINTS_LEFT, (student_id,))
            row = cur.fetchone()
            return row[0] if row else 0
    finally:
        release_conn(conn)


def get_max_level(student_id, lab, section):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(queries.GET_MAX_LEVEL, (student_id, lab, section))
            row = cur.fetchone()
            return row[0] if row else 0
    finally:
        release_conn(conn)


def update_hint_usage(student_id, lab, section, level):
    conn = get_conn()
    try:
        with conn.cursor() as cur:

            # ensure hint_usage row exists
            cur.execute("""
                INSERT INTO hint_usage(student_id, lab, section, max_level_used)
                VALUES (%s, %s, %s, 0)
                ON CONFLICT DO NOTHING
            """, (student_id, lab, section))

            # lock row to prevent race conditions
            cur.execute("""
                SELECT max_level_used
                FROM hint_usage
                WHERE student_id=%s AND lab=%s AND section=%s
                FOR UPDATE
            """, (student_id, lab, section))

            max_level = cur.fetchone()[0]

            # enforce level ordering
            if level != max_level + 1:
                conn.rollback()
                return False

            # atomic decrement hints
            cur.execute(queries.ATOMIC_DECREMENT_HINT, (student_id,))
            if cur.rowcount == 0:
                conn.rollback()
                return False

            # update level
            cur.execute(queries.UPSERT_LEVEL, (student_id, lab, section, level))

            conn.commit()
            return True

    finally:
        release_conn(conn)
