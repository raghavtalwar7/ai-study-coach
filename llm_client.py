from google import genai
from prompt_rules import SYSTEM_PROMPT
import streamlit as st

# Get API key from Streamlit secrets
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def ask_llm(mode, hint_level, student_context):
    prompt = f"""
{SYSTEM_PROMPT}
Mode: {mode}
Hint Level: {hint_level}
Student context:
{student_context}
Respond following all rules.
"""
    return client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    ).text
