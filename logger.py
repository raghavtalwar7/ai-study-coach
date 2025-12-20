def init_logs(session_state):
    if "logs" not in session_state:
        session_state.logs = []

def log_interaction(session_state, data):
    session_state.logs.append(data)
