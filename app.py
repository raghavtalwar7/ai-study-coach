import streamlit as st
from llm_client import ask_llm
from hint_manager import init_hints, init_student, use_hint, hints_left
from logger import init_logs, log_interaction

st.set_page_config(page_title="AI Study Coach", layout="centered")

# Init state
init_hints(st.session_state)
init_logs(st.session_state)

# UI
st.title("📘 AI Study Coach")

student_id = st.text_input("Enter your name (required)")

# Initialize student and show their hint count
if student_id:
    init_student(student_id, st.session_state)
    st.write(f"Hints left for **{student_id}**: **{hints_left(student_id, st.session_state)}**/15")
else:
    st.write("Please enter your name to see your hint balance")

mode = st.selectbox("Mode", ["Explainer", "Debugger"])
hint_level = st.selectbox("Hint Level", [1, 2, 3])
student_context = st.text_area(
    "Paste output or describe your issue",
    height=150
)

if st.button("Get Hint"):
    if not student_id:
        st.error("Please enter your name first")
    elif not use_hint(student_id, st.session_state):
        st.error("No hints left ❌")
    else:
        response = ask_llm(mode, hint_level, student_context)
        log_interaction(
            st.session_state,
            {
                "student_id": student_id,
                "mode": mode,
                "level": hint_level,
                "input": student_context,
                "response": response,
                "hints_remaining": hints_left(student_id, st.session_state)
            }
        )
        st.success("Hint")
        st.write(response)
        st.info(f"You have {hints_left(student_id, st.session_state)} hints remaining")

with st.expander("📜 Interaction Log"):
    st.json(st.session_state.logs)
