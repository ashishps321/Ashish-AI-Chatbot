# main imports
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env (for local dev)
load_dotenv()

# API Key Setup
API_KEY = None
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Google API key not found. Add it to Streamlit Secrets or .env")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(question: str):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# ------------------ Session State ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input_value" not in st.session_state:
    st.session_state.user_input_value = ""

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="ApkaApna AI Chatbot", page_icon="🤖", layout="wide")

# ------------------ Sidebar ------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("💬 ApkaApna AI Chatbot")
    st.markdown("---")
    st.subheader("⚡ About")
    st.write(
        """
        Welcome to **ApkaApna AI Chatbot**, your intelligent virtual assistant  
        designed to provide instant, accurate, and engaging responses.  
        """
    )
    st.subheader("✨ Key Highlights")
    st.markdown(
        """
        ✅ **Smart & Reliable** – Accurate answers powered by Google Gemini  
        💬 **Human-like Chat** – Natural and engaging conversations  
        ⚡ **Fast & Responsive** – Quick replies for smooth experience  
        🎯 **Personalized Help** – Tailored responses just for you  
        🔒 **Secure & Private** – Your chats stay safe and confidential  
        🌐 **Always Available** – 24/7 assistance, anytime you need  
        """
    )
    st.subheader("🛠 Options")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.user_input_value = ""
        st.experimental_rerun()
    st.markdown("---")
    st.caption("🚀 Developed by Ashish")

# ------------------ Custom ChatGPT Style ------------------
st.markdown("""
<style>
body {background-color:#f7f8fa; font-family:"Segoe UI", sans-serif;}
.chat-container {max-width:800px;margin:auto;padding:20px;}
.msg-row {display:flex;margin:12px 0;}
.msg-row.user {justify-content:flex-end;}
.msg-row.bot {justify-content:flex-start;}
.user-msg,.bot-msg {padding:12px 16px;border-radius:18px;max-width:70%;font-size:16px;line-height:1.4;word-wrap:break-word;box-shadow:0 2px 6px rgba(0,0,0,0.1);}
.user-msg {background-color:#0d6efd;color:white;border-bottom-right-radius:5px;}
.bot-msg {background-color:#e9ecef;color:#212529;border-bottom-left-radius:5px;}
.title {text-align:center;font-size:32px;font-weight:bold;color:#0d47a1;margin-bottom:4px;}
.tagline {text-align:center;font-size:14px;color:#6c757d;margin-bottom:25px;}
.input-container {position:fixed;bottom:15px;width:80%;left:50%;transform:translateX(-50%);background:white;padding:10px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.1);display:flex;gap:10px;z-index:999;}
.stTextInput {flex:1;}
.stButton>button {background-color:#0d6efd;color:white;padding:0.6rem 1rem;border-radius:8px;border:none;cursor:pointer;font-weight:bold;}
.stButton>button:hover {background-color:#0b5ed7;}
</style>
""", unsafe_allow_html=True)

# ------------------ Main Chat Area ------------------
st.markdown('<div class="title">🤖 ApkaApna AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">“Ask anything, get instant answers – powered by AI & Developed by ABSingh”</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Show chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="msg-row user"><div class="user-msg">{msg}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-row bot"><div class="bot-msg">{msg}</div></div>', unsafe_allow_html=True)

# Input + Ask button
st.markdown('<div class="input-container">', unsafe_allow_html=True)
col1, col2 = st.columns([8,1])
with col1:
    user_input = st.text_input(
        "💭 Type your message:",
        key="chat_input",
        label_visibility="collapsed",
        placeholder="Send a message...",
        value=st.session_state.user_input_value
    )
with col2:
    send = st.button("Ask")
st.markdown('</div>', unsafe_allow_html=True)

# Handle submission
if (send and user_input.strip()):
    st.session_state.chat_history.append(("user", user_input))
    response = get_gemini_response(user_input)
    st.session_state.chat_history.append(("bot", response))

    # Reset input safely
    st.session_state.user_input_value = ""
    st.experimental_rerun()

# Handle Enter key press
if user_input.strip() and not send:
    st.session_state.user_input_value = user_input
