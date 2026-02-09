from student_repo import get_hints_left, update_hint_usage

def hints_left(student_id):
    return get_hints_left(student_id)

def register_hint(student_id, lab, section, level):
    return update_hint_usage(student_id, lab, section, level)
