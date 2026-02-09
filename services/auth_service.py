from student_repo import fetch_student, init_hint_balance

def authenticate_student(student_id):
    student = fetch_student(student_id)
    if not student:
        return False

    if not student[1]:  # active flag
        return False

    init_hint_balance(student_id)
    return True
