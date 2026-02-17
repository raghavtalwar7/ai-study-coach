import streamlit as st
from llm_client import ask_llm
from lab3_hint_policy import LAB3_HINT_POLICY
from services.auth_service import authenticate_student
from services.hint_service import hints_left, register_hint
from logger import init_logs, log_interaction

st.set_page_config(page_title="AI Study Coach", layout="centered")

# -------------------
# Read query parameters from URL (notebook or link)
# -------------------
lab = st.query_params.get("lab", "lab3")
context = st.query_params.get("context", "")
section_param = st.query_params.get("section", None) # can be None
mode_param = st.query_params.get("mode", None)        # can be None
hint_level_param = st.query_params.get("hint_level", None)  # can be None

if not lab:
    lab = "lab3"

# Init state
init_logs(st.session_state)

# UI
st.title("AI Study Coach")


# Use session_state for persistence
if "student_id" not in st.session_state:
    st.session_state.student_id = ""

student_id = st.text_input(
    "Enter your student id (required)",
    value=st.session_state.student_id,
    key="student_id_input",
    on_change=lambda: setattr(st.session_state, 'student_id', st.session_state.student_id_input)
)

# Update from input immediately
st.session_state.student_id = student_id


# Initialize student and show their hint count
if student_id:
    if not authenticate_student(student_id):
        st.error("Unauthorized student ID ❌")
        st.stop()
    st.write(f"Hints left for **{student_id}**: **{hints_left(student_id)}**/15")
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

# Prevent double-click / parallel requests in UI
if "busy" not in st.session_state:
    st.session_state.busy = False


if st.button("Get Hint", disabled=st.session_state.busy):
    st.session_state.busy = True
    try:
        if not student_id:
            st.error("Please enter your id first")
            st.stop()

        success = register_hint(student_id, lab, section, hint_level)

        if not success:
            st.error(
                "Hint request denied ❌\n\n"
                "Possible reasons:\n"
                "- No hints left\n"
                "- Hint levels must be requested in order (1 → 2 → 3)"
            )
            st.stop()

        st.success("Hint granted ✅")

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
                "hints_remaining": hints_left(student_id)
            }
        )

        st.success("Hint provided")
        st.write(response)
        st.info(f"You have {hints_left(student_id)} hints remaining")

    finally:
        st.session_state.busy = False

with st.expander("Interaction Log"):
    st.json(st.session_state.logs)
