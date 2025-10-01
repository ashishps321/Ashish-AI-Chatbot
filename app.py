import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from io import BytesIO
from pydub import AudioSegment

# Optional: only for local mic capture
try:
    import speech_recognition as sr
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

# Load environment variables
load_dotenv()

# Get API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Google API key not found. Add it to Streamlit Secrets or .env")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
MODEL_NAME = "models/gemini-2.0-flash"
model = genai.GenerativeModel(MODEL_NAME)

# Function to get response
def get_gemini_response(question: str):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Initialize chat history and input safely
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
    st.subheader("🛠 Options")
    if st.button("🧹 Clear Chat"):
        st.session_state["chat_history"] = []
    st.markdown("---")
    st.caption("🚀 Developed by Ashish")

# Display chat history
for role, msg in st.session_state["chat_history"]:
    if role == "user":
        st.markdown(f'<div style="color:white;background:#0d6efd;padding:8px;border-radius:8px;margin:5px;">You: {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="background:#e9ecef;padding:8px;border-radius:8px;margin:5px;">Bot: {msg}</div>', unsafe_allow_html=True)

# Input form
with st.form(key="chat_form"):
    user_input = st.text_input("💭 Type your message:", placeholder="Type your question here...", key="current_input")
    
    # Audio upload
    audio_file = st.file_uploader("🎤 Or upload audio (.wav/.mp3)", type=["wav","mp3"])
    
    # Live microphone (local only)
    if MIC_AVAILABLE:
        if st.button("🎙 Record via Microphone"):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening... Speak now")
                audio_data = r.listen(source)
                try:
                    user_input = r.recognize_google(audio_data)
                    st.success(f"You said: {user_input}")
                except Exception as e:
                    st.error(f"Audio recognition failed: {str(e)}")

    submit_button = st.form_submit_button("Ask")

# Handle submission
if submit_button:
    user_message = None

    # Priority: audio upload
    if audio_file is not None:
        r = sr.Recognizer()
        # Convert mp3 to wav if needed
        from tempfile import NamedTemporaryFile
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
    elif user_input.strip():
        user_message = user_input.strip()
        st.session_state["chat_history"].append(("user", user_message))

    # Get AI response
    if user_message:
        response = get_gemini_response(user_message)
        st.session_state["chat_history"].append(("bot", response))
        st.session_state["current_input"] = ""
