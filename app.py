# main imports
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# load .env for local development (no effect on Streamlit Cloud)
load_dotenv()

# Try Streamlit secrets first (when deployed), otherwise fallback to environment variable (local)
API_KEY = None
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Google API key not found. Add it to Streamlit Secrets (recommended) or put it in a local .env file for development.")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(question: str):
    response = model.generate_content(question)
    return response.text

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="AI Chatbot by ASHISH", page_icon="🤖", layout="wide")

# ------------------ Sidebar ------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("💬 Ashish's AI Chatbot")
    st.markdown("---")

    st.subheader("⚡ About")
    st.write(
        """
        Welcome to **Ashish’s AI Chatbot**, your intelligent virtual assistant  
        designed to provide instant, accurate, and engaging responses.  
        """
    )

    st.subheader("✨ Key Highlights")
    st.markdown(
        """
        ✅ **Smart & Reliable** –Highly accurate answer  
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
        st.rerun()

    st.markdown("---")
    st.caption("🚀 Developed by Ashish")

# ------------------ Session State ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ Custom ChatGPT Style ------------------
st.markdown(
    """
    <style>
    /* Overall App */
    body {
        background-color: #f7f8fa;
        font-family: "Segoe UI", sans-serif;
    }
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }

    /* User and Bot messages */
    .msg-row {
        display: flex;
        margin: 12px 0;
    }
    .msg-row.user {
        justify-content: flex-end;
    }
    .msg-row.bot {
        justify-content: flex-start;
    }

    .user-msg, .bot-msg {
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 70%;
        font-size: 16px;
        line-height: 1.4;
        word-wrap: break-word;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    /* User bubble */
    .user-msg {
        background-color: #0d6efd;
        color: white;
        border-bottom-right-radius: 5px;
    }

    /* Bot bubble */
    .bot-msg {
        background-color: #e9ecef;
        color: #212529;
        border-bottom-left-radius: 5px;
    }

    /* Title & tagline */
    .title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #0d47a1;
        margin-bottom: 4px;
    }
    .tagline {
        text-align: center;
        font-size: 14px;
        color: #6c757d;
        margin-bottom: 25px;
    }

    /* Input section sticky bottom */
    .input-container {
        position: fixed;
        bottom: 15px;
        width: 80%;
        left: 50%;
        transform: translateX(-50%);
        background: white;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        gap: 10px;
        z-index: 999;
    }
    .stTextInput {
        flex: 1;
    }
    .stButton > button {
        background-color: #0d6efd;
        color: white;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0b5ed7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ Main Chat Area ------------------
st.markdown('<div class="title">🤖 Ashish\'s AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">“ChatGPT style conversation UI”</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Show chat history
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(
                f"""
                <div class="msg-row user">
                    <div class="user-msg">{msg}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="msg-row bot">
                    <div class="bot-msg">{msg}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Input + Button section
    with st.container():
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([8,1])
        with col1:
            user_input = st.text_input("💭 Type your message:", key="input", label_visibility="collapsed", placeholder="Send a message...")
        with col2:
            send = st.button("Ask")

        st.markdown('</div>', unsafe_allow_html=True)

        if (user_input and user_input.strip() and send) or (user_input and user_input.strip() and not send and st.session_state.input):
            # Add user msg
            st.session_state.chat_history.append(("user", user_input))

            # Get bot reply
            response = get_gemini_response(user_input)
            st.session_state.chat_history.append(("bot", response))

            # Clear input
            st.session_state.input = ""
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
