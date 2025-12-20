import json
import os
from pathlib import Path

MAX_HINTS = 15
HINTS_FILE = "student_hints.json"

def load_hints():
    """Load hint data from file"""
    if os.path.exists(HINTS_FILE):
        with open(HINTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hints(hints_data):
    """Save hint data to file"""
    with open(HINTS_FILE, 'w') as f:
        json.dump(hints_data, f, indent=2)

def init_hints(session_state):
    """Initialize the student hint store from persistent storage"""
    if "student_hints" not in session_state:
        session_state.student_hints = load_hints()

def init_student(student_id, session_state):
    """Initialize a specific student's hint count"""
    if student_id not in session_state.student_hints:
        session_state.student_hints[student_id] = MAX_HINTS
        save_hints(session_state.student_hints)

def use_hint(student_id, session_state):
    """Use one hint for a student. Returns True if successful, False if no hints left"""
    if session_state.student_hints[student_id] <= 0:
        return False
    session_state.student_hints[student_id] -= 1
    save_hints(session_state.student_hints)
    return True

def hints_left(student_id, session_state):
    """Get remaining hints for a student"""
    return session_state.student_hints[student_id]
