import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# ------------------ LOAD API KEY ------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")   # ← FIXED (Use a clean variable)

if not api_key:
    st.error("❌ API key not found! Add GEMINI_API_KEY to your .env file.")
    st.stop()

# ------------------ CREATE GEMINI CLIENT ------------------
client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"

# ------------------ STREAMLIT UI ------------------
st.title("⚡ EV Chatbot (Gemini AI)")
st.write("Ask anything related to Electric Vehicles!")

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ FUNCTION TO GET GEMINI RESPONSE ------------------
def ask_gemini(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    # Gemini returns list of parts → extract text safely
    try:
        return response.text
    except:
        return "❌ Could not read response."

# ------------------ DISPLAY CHAT HISTORY ------------------
for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)

# ------------------ USER INPUT ------------------
user_msg = st.chat_input("Type your EV question...")

if user_msg:
    # Add user message
    st.session_state.history.append(("user", user_msg))

    # Get response
    reply = ask_gemini(user_msg)

    # Add bot response
    st.session_state.history.append(("assistant", reply))

    # Rerun to refresh UI
    st.rerun()

