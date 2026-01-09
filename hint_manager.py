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
        session_state.student_hints[student_id] = {
            "remaining": MAX_HINTS,
            "sections": {}
        }
        save_hints(session_state.student_hints)

def hints_left(student_id, session_state):
    """Get remaining hints for a student"""
    return session_state.student_hints.get(student_id, {}).get("remaining", 0)

def _section_key(lab, section):
    return f"{lab}::{section}"

def can_use_level(student_id, lab, section, requested_level, session_state):
    """
    Enforce progressive hint ladder:
    Level n can only be used if max_level_used == n-1
    """
    student = session_state.student_hints.get(student_id)
    if not student:
        return False

    section_key = _section_key(lab, section)
    section_state = student["sections"].get(section_key, {"max_level_used": 0})

    return requested_level == section_state["max_level_used"] + 1


def register_hint_use(student_id, lab, section, level, session_state):
    """
    Register a hint usage:
    - decrement global budget
    - update max level used for this section
    """
    student = session_state.student_hints.get(student_id)
    if not student:
        return

    if student["remaining"] <= 0:
        return

    section_key = _section_key(lab, section)

    if section_key not in student["sections"]:
        student["sections"][section_key] = {"max_level_used": 0}

    student["sections"][section_key]["max_level_used"] = level
    student["remaining"] -= 1
    save_hints(session_state.student_hints)
