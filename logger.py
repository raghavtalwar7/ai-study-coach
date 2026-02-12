from student_repo import insert_log, get_student_mode_counts


def init_logs(session_state):
    if "logs" not in session_state:
        session_state.logs = []

def log_interaction(session_state, data):
    """Log interaction to session state and persist to database."""
    session_state.logs.append(data)
    
    # Persist to database
    insert_log(
        student_id=data.get("student_id"),
        lab=data.get("lab"),
        section=data.get("section"),
        mode=data.get("mode"),
        hint_level=data.get("level"),
        user_input=data.get("input"),
        response=data.get("response"),
        hints_remaining=data.get("hints_remaining")
    )


def get_usage_stats(student_id):
    """Get how many times a student used each mode (explainer/debugger)."""
    return get_student_mode_counts(student_id)
