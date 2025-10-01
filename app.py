import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# File handling
try:
    from PyPDF2 import PdfReader
except ImportError:
    st.warning("PyPDF2 not installed. PDF upload won't work.")

try:
    import docx
except ImportError:
    st.warning("python-docx not installed. DOCX upload won't work.")

# Load environment variables
load_dotenv()
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Google API key not found!")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
MODEL_NAME = "models/gemini-2.0-flash"
model = genai.GenerativeModel(MODEL_NAME)

# Function to get AI response
def get_gemini_response(question: str):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Page config
st.set_page_config(page_title="Bharat Intelligence Chatbot", page_icon="🤖", layout="wide")

# Sidebar (left corner content unchanged)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("💬 Bharat Intelligence (BI) Chatbot")
    st.markdown("---")
    st.subheader("⚡ About")
    st.write("Welcome to **Bharat Intelligence (BI) Chatbot v1.0 – AI-powered assistant delivering instant, precise, and context-aware answers**")
    st.subheader("✨ Key Highlights")
    st.markdown("""
        ✅ **Smart & Reliable** – Highly Accurate Answer  
        💬 **Human-like Chat** – Natural and engaging conversations  
        ⚡ **Fast & Responsive** – Quick replies  
        🎯 **Personalized Help** – Tailored responses  
        🔒 **Secure & Private** – Safe & confidential  
        🌐 **Always Available** – 24/7 assistance
    """)
    st.subheader("🛠 Options")
    if st.button("🧹 Clear Chat"):
        st.session_state["chat_history"] = []
    st.markdown("---")
    st.caption("🚀 Developed by Ashish")

# Custom CSS
st.markdown("""
<style>
.user-bubble {background-color:#0d6efd;color:white;padding:12px;border-radius:18px;max-width:70%;margin-left:auto;margin-bottom:8px;word-wrap:break-word;}
.bot-bubble {background-color:#e9ecef;color:#212529;padding:12px;border-radius:18px;max-width:70%;margin-right:auto;margin-bottom:8px;word-wrap:break-word;}
.title {text-align:center;font-size:32px;font-weight:bold;color:#0d47a1;margin-bottom:4px;}
.tagline {text-align:center;font-size:14px;color:#6c757d;margin-bottom:15px;}
.stTextInput {flex:1;}
.stButton > button {background-color:#0d6efd;color:white;padding:0.6rem 1rem;border-radius:8px;border:none;cursor:pointer;font-weight:bold;}
.stButton > button:hover {background-color:#0b5ed7;}
.response-container {margin-top:10px;margin-bottom:20px;}
</style>
""", unsafe_allow_html=True)

# Title & description
st.markdown('<div class="title">🤖 Bharat Intelligence (BI) Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Your AI companion for fast, accurate, and insightful answers, powered by AI & developed by ABSingh</div>', unsafe_allow_html=True)

# File uploader (always available, top of chat input)
uploaded_files = st.file_uploader(
    "📎 Upload files (txt, pdf, docx, png, jpg, jpeg, bmp) at any time", 
    type=["txt","pdf","docx","png","jpg","jpeg","bmp"], 
    accept_multiple_files=True
)

# Chat input using form
with st.form("chat_form"):
    user_input = st.text_input("💭 Type your message:", key="user_input_key")
    submit_button = st.form_submit_button("Ask")

# Process input and files
if submit_button and user_input.strip():
    combined_input = user_input.strip()
    st.session_state["chat_history"].append(("user", combined_input))

    # Process uploaded files (any time)
    if uploaded_files:
        file_texts = []
        for file in uploaded_files:
            if file.type == "text/plain":
                file_texts.append(file.read().decode("utf-8"))
            elif file.type == "application/pdf":
                reader = PdfReader(file)
                text = "".join([page.extract_text() + "\n" for page in reader.pages])
                file_texts.append(text)
            elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               "application/msword"]:
                doc = docx.Document(file)
                text = "\n".join([p.text for p in doc.paragraphs])
                file_texts.append(text)
            elif file.type.startswith("image/"):
                st.session_state["chat_history"].append(("user", f"[Uploaded Image] {file.name}"))
        if file_texts:
            combined_files_text = "\n".join(file_texts)
            st.session_state["chat_history"].append(("user", f"[Uploaded Files] {combined_files_text}"))
            combined_input += "\n" + combined_files_text

    # Get AI response
    response_text = get_gemini_response(combined_input)
    st.session_state["chat_history"].append(("bot", response_text))

# Display chat history just above input
for role, msg in st.session_state["chat_history"]:
    if role == "user":
        st.markdown(f'<div class="user-bubble">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble response-container">{msg}</div>', unsafe_allow_html=True)
