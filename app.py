import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
load_dotenv()

# API Key
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Google API key not found. Add it to Streamlit Secrets or .env")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
MODEL_NAME = "models/gemini-2.0-flash"
model = genai.GenerativeModel(MODEL_NAME)

def get_gemini_response(question: str):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_input" not in st.session_state:
    st.session_state.current_input = ""

# Page config
st.set_page_config(page_title="Bharat Intelligence (BI) Chatbot", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("💬 Bharat Intelligence (BI) Chatbot")
    st.markdown("---")
    st.subheader("⚡ About")
    st.write("Welcome to **Bharat Intelligence (BI) Chatbot v1.0 – An AI-powered assistant delivering instant, precise, and context-aware answers")
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
        st.session_state.chat_history = []
    st.markdown("---")
    st.caption("🚀 Developed by Ashish")

# Custom CSS
st.markdown("""
<style>
.chat-container {max-width:800px;margin:auto;padding:20px;}
.msg-row {display:flex;margin:12px 0;}
.msg-row.user {justify-content:flex-end;}
.msg-row.bot {justify-content:flex-start;}
.user-msg,.bot-msg {padding:12px 16px;border-radius:18px;max-width:70%;font-size:16px;line-height:1.4;word-wrap:break-word;box-shadow:0 2px 6px rgba(0,0,0,0.1);}
.user-msg {background-color:#0d6efd;color:white;border-bottom-right-radius:5px;}
.bot-msg {background-color:#e9ecef;color:#212529;border-bottom-left-radius:5px;}
.title {text-align:center;font-size:32px;font-weight:bold;color:#0d47a1;margin-bottom:4px;}
.tagline {text-align:center;font-size:14px;color:#6c757d;margin-bottom:25px;}
.stTextInput {flex:1;}
.stButton > button {background-color:#0d6efd;color:white;padding:0.6rem 1rem;border-radius:8px;border:none;cursor:pointer;font-weight:bold;}
.stButton > button:hover {background-color:#0b5ed7;}
</style>
""", unsafe_allow_html=True)

# Main chat area
st.markdown('<div class="title">🤖 Bharat Intelligence (BI) Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">“Welcome to Bharat Intelligence (BI) Chatbot – your AI companion for fast, accurate, and insightful answers, powered by AI & developed by ABSingh”</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="msg-row user"><div class="user-msg">{msg}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-row bot"><div class="bot-msg">{msg}</div></div>', unsafe_allow_html=True)

# Input + submit button (without form)
user_input = st.text_input("💭 Type your message:", placeholder="Send a message...", value=st.session_state.current_input)

if st.button("Ask") and user_input.strip():
    # Append user message
    st.session_state.chat_history.append(("user", user_input.strip()))
    
    # Get response from Gemini
    response = get_gemini_response(user_input.strip())
    st.session_state.chat_history.append(("bot", response))
    
    # Clear input
    st.session_state.current_input = ""
