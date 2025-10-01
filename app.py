import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from io import BytesIO
import requests

# Load environment variables
load_dotenv()

# Get Google Gemini API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Google API key not found. Add it to Streamlit Secrets or .env")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
MODEL_NAME = "models/gemini-2.0-flash"
model = genai.GenerativeModel(MODEL_NAME)

# Function to get response from Gemini
def get_gemini_response(question: str):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Function to transcribe audio using Hugging Face Whisper API (free)
def transcribe_audio(file_bytes):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
    headers = {"Authorization": f"Bearer {st.secrets.get('HF_API_KEY', '')}"}
    response = requests.post(API_URL, headers=headers, files={"file": file_bytes})
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        return "[Audio transcription failed]"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "current_input" not in st.session_state:
    st.session_state["current_input"] = ""

# Page config
st.set_page_config(page_title="Bharat Intelligence (BI) Chatbot", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("💬 Bharat Intelligence (BI) Chatbot")
    st.markdown("---")
    st.subheader("✨ Options")
    if st.button("🧹 Clear Chat"):
        st.session_state["chat_history"] = []
    st.markdown("---")
    st.caption("🚀 Developed by Ashish")

# Display chat history
for role, msg in st.session_state["chat_history"]:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")

# Input form
with st.form(key="chat_form"):
    user_input = st.text_input("💭 Type your message:", placeholder="Type your question here...", key="current_input")
    audio_file = st.file_uploader("🎤 Or upload audio (.wav/.mp3)", type=["wav","mp3"])
    submit_button = st.form_submit_button("Ask")

if submit_button:
    user_message = None

    # Handle audio upload
    if audio_file is not None:
        audio_bytes = BytesIO(audio_file.read())
        user_message = transcribe_audio(audio_bytes)
        st.session_state["chat_history"].append(("user", f"[Audio] {user_message}"))

    elif st.session_state.get("current_input", "").strip():
        user_message = st.session_state["current_input"].strip()
        st.session_state["chat_history"].append(("user", user_message))

    # Get AI response if message exists
    if user_message:
        response = get_gemini_response(user_message)
        st.session_state["chat_history"].append(("bot", response))
        st.session_state["current_input"] = ""
