import streamlit as st
from llm_client import ask_llm
from lab5_hint_policy import LAB5_HINT_POLICY
from services.auth_service import authenticate_student
from services.hint_service import hints_left, register_hint
from logger import init_logs, log_interaction

st.set_page_config(page_title="AI Study Coach", layout="centered")

# -------------------
# Read query parameters from URL (notebook or link)
# -------------------
lab = st.query_params.get("lab", "lab5")
context = st.query_params.get("context", "")
section_param = st.query_params.get("section", None) # can be None
mode_param = st.query_params.get("mode", None)        # can be None
hint_level_param = st.query_params.get("hint_level", None)  # can be None

if not lab:
    lab = "lab5"

# Init state
init_logs(st.session_state)

# UI
st.title("AI Study Coach")


# Use session_state for persistence
if "student_id" not in st.session_state:
    st.session_state.student_id = ""

if "section" not in st.session_state:
    st.session_state.section = "info"

if "mode" not in st.session_state:
    st.session_state.mode = "explainer"

if "hint_level" not in st.session_state:
    st.session_state.hint_level = 1

if "busy" not in st.session_state:
    st.session_state.busy = False

student_id = st.text_input(
    "Enter your student id (required)",
    value=st.session_state.student_id,
    key="student_id_input"
)

# Update state from input
st.session_state.student_id = student_id

# Initialize student and show their hint count
if student_id:
    if not authenticate_student(student_id):
        st.error("Unauthorized student ID ❌")
        st.stop()
    st.write(f"Hints left for **{student_id}**: **{hints_left(student_id)}**/15")
else:
    st.write("Please enter your id to see your hint balance")

sections = ["classification", "confusion_matrix", "plots", "regression", "regression_metrics", "residual"]
if section_param in sections:
    st.session_state.section = section_param
else:
    st.session_state.section = st.selectbox(
        "Select Lab Section",
        sections,
        index=sections.index(st.session_state.section) if st.session_state.section in sections else 0,
        key="section_selector"
    )

modes = ["Explainer", "Debugger"]
if mode_param and mode_param.lower() in ["explainer", "debugger"]:
    st.session_state.mode = mode_param.lower()
else:
    mode_index = 0 if st.session_state.mode.lower() == "explainer" else 1
    selected_mode = st.selectbox(
        "Mode",
        modes,
        index=mode_index,
        key="mode_selector"
    )
    st.session_state.mode = selected_mode.lower()

if hint_level_param and hint_level_param in ["1","2","3"]:
    st.session_state.hint_level = int(hint_level_param)
else:
    st.session_state.hint_level = st.selectbox(
        "Hint Level",
        [1, 2, 3],
        index=st.session_state.hint_level - 1,
        key="hint_level_selector"
    )

student_context = st.text_area(
    "Paste output or describe your issue",
    height=150
)

# Handle Get Hint button click
if st.button("Get Hint", disabled=(not student_id) or st.session_state.busy):
    st.session_state.busy = True
    
    try:
        if not student_id:
            st.error("Please enter your id first")
        else:
            success = register_hint(student_id, lab, st.session_state.section, st.session_state.hint_level)

            if not success:
                st.error(
                    "Hint request denied ❌\n\n"
                    "Possible reasons:\n"
                    "- No hints left\n"
                    "- Hint levels must be requested in order (1 → 2 → 3)"
                )
            else:
                try:
                    rule = LAB5_HINT_POLICY[st.session_state.mode][st.session_state.section][st.session_state.hint_level]
                except KeyError:
                    st.error("Invalid hint request for this lab section.")
                else:
                    st.success("Hint granted ✅")

                    response = ask_llm(
                        mode=st.session_state.mode,
                        level=st.session_state.hint_level,
                        section=st.session_state.section,
                        rule=rule,
                        context=context,
                        user_input=student_context
                    )

                    log_interaction(
                        st.session_state,
                        {
                            "student_id": student_id,
                            "lab": lab,
                            "section": st.session_state.section,
                            "mode": st.session_state.mode,
                            "level": st.session_state.hint_level,
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
        # Always reset busy flag
        st.session_state.busy = False

with st.expander("Interaction Log"):
    st.json(st.session_state.logs)
