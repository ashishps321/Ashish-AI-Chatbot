import streamlit as st
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from io import BytesIO
from pydub import AudioSegment

# Optional: live mic (local only)
try:
    import speech_recognition as sr
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

# Load env
load_dotenv()

API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Google API key not found!")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
MODEL_NAME = "models/gemini-2.0-flash"
model = genai.GenerativeModel(MODEL_NAME)

def get_gemini_response(question: str):
    """Get response from Gemini AI"""
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "current_input" not in st.session_state:
    st.session_state["current_input"] = ""

# Page config
st.set_page_config(page_title="Bharat Intelligence Chatbot", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("💬 Bharat Intelligence (BI) Chatbot")
    if st.button("🧹 Clear Chat"):
        st.session_state["chat_history"] = []

# Display chat history
for role, msg in st.session_state["chat_history"]:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")

# Input form
with st.form("chat_form"):
    user_input = st.text_input("💭 Type your message:", key="current_input")
    
    # Live mic input
    if MIC_AVAILABLE:
        if st.button("🎙 Speak"):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening... Speak now")
                audio_data = r.listen(source)
                try:
                    user_input = r.recognize_google(audio_data)
                    st.success(f"You said: {user_input}")
                except Exception as e:
                    st.error(f"Audio recognition failed: {str(e)}")

    # Audio file upload fallback
    audio_file = st.file_uploader("🎤 Or upload audio (.wav/.mp3)", type=["wav", "mp3"])

    submit_button = st.form_submit_button("Ask")

# Handle submission
if submit_button:
    user_message = None

    # Audio file upload handling
    if audio_file is not None:
        from tempfile import NamedTemporaryFile
        import speech_recognition as sr
        r = sr.Recognizer()
        with NamedTemporaryFile(suffix=".wav") as temp_wav_file:
            if audio_file.type == "audio/mpeg":
                audio_segment = AudioSegment.from_file(BytesIO(audio_file.read()), format="mp3")
                audio_segment.export(temp_wav_file.name, format="wav")
            else:
                temp_wav_file.write(audio_file.read())
                temp_wav_file.flush()
            with sr.AudioFile(temp_wav_file.name) as source:
                audio_data = r.record(source)
                try:
                    user_message = r.recognize_google(audio_data)
                    st.session_state["chat_history"].append(("user", f"[Audio] {user_message}"))
                except Exception as e:
                    st.error(f"Audio recognition failed: {str(e)}")
    
    # Text input handling
    elif user_input.strip():
        user_message = user_input.strip()
        st.session_state["chat_history"].append(("user", user_message))

    # Get AI response with streaming effect
    if user_message:
        bot_msg = ""
        response = get_gemini_response(user_message)
        # Simulate streaming line by line
        for line in response.split(". "):
            bot_msg += line + ". "
            if st.session_state["chat_history"] and st.session_state["chat_history"][-1][0] == "bot":
                st.session_state["chat_history"][-1] = ("bot", bot_msg)
            else:
                st.session_state["chat_history"].append(("bot", bot_msg))
            time.sleep(0.1)  # small delay for typing effect
        st.session_state["current_input"] = ""
