import streamlit as st
from llm_client import ask_llm
from lab3_hint_policy import LAB3_HINT_POLICY
from hint_manager import init_hints, init_student, can_use_level, register_hint_use, hints_left
from logger import init_logs, log_interaction

st.set_page_config(page_title="AI Study Coach", layout="centered")

# -------------------
# Read query parameters from URL (notebook or link)
# -------------------
lab = st.query_params.get("lab", ["lab3"])[0]
context = st.query_params.get("context", [""])[0]
section_param = st.query_params.get("section", [None])[0]  # can be None
mode_param = st.query_params.get("mode", [None])[0]        # can be None
hint_level_param = st.query_params.get("hint_level", [None])[0]  # can be None

if lab != "lab3":
    st.error("This AI coach is only available for Lab 3.")
    st.stop()

# Init state
init_hints(st.session_state)
init_logs(st.session_state)

# UI
st.title("📘 AI Study Coach")

student_id = st.text_input("Enter your student id (required)")

# Initialize student and show their hint count
if student_id:
    init_student(student_id, st.session_state)
    st.write(f"Hints left for **{student_id}**: **{hints_left(student_id, st.session_state)}**/15")
else:
    st.write("Please enter your id to see your hint balance")

sections = ["info", "missing", "outliers", "correlation", "chi_square"]
if section_param in sections:
    section = section_param
else:
    section = st.selectbox("Select Lab Section", sections)

modes = ["Explainer", "Debugger"]
if mode_param and mode_param.lower() in ["explainer", "debugger"]:
    mode = mode_param.lower()
else:
    mode_ui = st.selectbox("Mode", modes)
    mode = mode_ui.lower()

if hint_level_param and hint_level_param in ["1","2","3"]:
    hint_level = int(hint_level_param)
else:
    hint_level = st.selectbox("Hint Level", [1, 2, 3])

student_context = st.text_area(
    "Paste output or describe your issue",
    height=150
)

if st.button("Get Hint"):
    if not student_id:
        st.error("Please enter your id first")
        st.stop()
    if not can_use_level(student_id, lab, section, hint_level, st.session_state):
        st.error(
            "You must request hints in order: "
            "Level 1 → Level 2 → Level 3."
        )
        st.stop()
    if hints_left(student_id, st.session_state) <= 0:
        st.error("No hints left ❌")
        st.stop()
    try:
        rule = LAB3_HINT_POLICY[mode][section][hint_level]
    except KeyError:
        st.error("Invalid hint request for this lab section.")
        st.stop()

    response = ask_llm(
        mode=mode,
        level=hint_level,
        section=section,
        rule=rule,
        context=context,
        user_input=student_context
    )

    register_hint_use(student_id, lab, section, hint_level, st.session_state)

    log_interaction(
        st.session_state,
        {
            "student_id": student_id,
            "lab": lab,
            "section": section,
            "mode": mode,
            "level": hint_level,
            "rule": rule,
            "input": student_context,
            "response": response,
            "hints_remaining": hints_left(student_id, st.session_state)
        }
    )
    st.success("Hint provided")
    st.write(response)
    st.info(f"You have {hints_left(student_id, st.session_state)} hints remaining")

with st.expander("📜 Interaction Log"):
    st.json(st.session_state.logs)
