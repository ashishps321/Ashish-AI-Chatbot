# main imports
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# ------------------ API Setup ------------------
# load .env for local development (no effect on Streamlit Cloud)
load_dotenv()

# Try Streamlit secrets first (when deployed), otherwise fallback to environment variable (local)
API_KEY = None
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ Google API key not found. Add it to Streamlit Secrets or .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(question: str):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

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
        Welcome to **Ashish’s AI Chatbot** 🚀  
        - 💡 Insightful Responses  
        - 🗣️ Natural Conversation  
        - 🎯 Personalized Interaction  
        - ⚡ Fast & Efficient  
        """
    )

    st.subheader("🎨 Theme")
    theme = st.radio("Choose theme:", ["Light", "Dark"], index=0)

    st.subheader("🛠 Options")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

    st.markdown("---")
    st.caption("Developed by Ashish")

# ------------------ Session State ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ Main Chat Area ------------------
st.markdown('<div class="title">🤖 Ashish\'s AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">“Your AI companion for knowledge and conversation.”</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Display chat history (persists)
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(
                f"""
                <div class="msg-row user">
                    <div class="user-msg">{msg}</div>
                    <img src="https://cdn-icons-png.flaticon.com/512/1946/1946429.png" class="msg-avatar">
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="msg-row bot">
                    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" class="msg-avatar">
                    <div class="bot-msg">{msg}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Input at bottom
    user_input = st.text_input("💭 Type your message:", key="input", placeholder="Ask me anything...")

    if st.button(" Submit ", use_container_width=True):
        if user_input.strip():
            # Add user msg
            st.session_state.chat_history.append(("user", user_input))

            # Get bot reply
            response = get_gemini_response(user_input)
            st.session_state.chat_history.append(("bot", response))
        else:
            st.warning("⚠️ Please enter a question.")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ Apply Themes ------------------
if theme == "Light":
    st.markdown(
        """
        <style>
        body { background: linear-gradient(135deg, #f9f9f9 0%, #e3f2fd 100%); }
        .chat-container { max-width: 750px; margin: auto; padding: 20px; }
        .user-msg, .bot-msg {
            padding: 12px 16px; border-radius: 15px; margin: 10px 0;
            font-size: 16px; display: inline-block; max-width: 80%;
            backdrop-filter: blur(8px); box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        }
        .user-msg { background: rgba(72, 187, 120, 0.9); color: white; text-align: right; }
        .bot-msg { background: rgba(255, 255, 255, 0.7); color: #2c3e50; text-align: left; }
        .msg-row { display: flex; align-items: flex-start; margin-bottom: 10px; }
        .msg-row.user { justify-content: flex-end; }
        .msg-avatar { width: 42px; height: 42px; border-radius: 50%; margin: 0 8px; }
        .title { text-align: center; font-size: 34px; font-weight: bold; color: #0d47a1; }
        .tagline { text-align: center; font-size: 16px; font-style: italic; color: #546e7a; }
        </style>
        """,
        unsafe_allow_html=True,
    )

elif theme == "Dark":
    st.markdown(
        """
        <style>
        body { background: linear-gradient(135deg, #1e1e2f 0%, #121212 100%); color: white; }
        .chat-container { max-width: 750px; margin: auto; padding: 20px; }
        .user-msg, .bot-msg {
            padding: 12px 16px; border-radius: 15px; margin: 10px 0;
            font-size: 16px; display: inline-block; max-width: 80%;
            backdrop-filter: blur(8px); box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
        }
        .user-msg { background: rgba(0, 200, 83, 0.9); color: white; text-align: right; }
        .bot-msg { background: rgba(33, 33, 33, 0.8); color: #f1f1f1; text-align: left; }
        .msg-row { display: flex; align-items: flex-start; margin-bottom: 10px; }
        .msg-row.user { justify-content: flex-end; }
        .msg-avatar { width: 42px; height: 42px; border-radius: 50%; margin: 0 8px; }
        .title { text-align: center; font-size: 34px; font-weight: bold; color: #00e5ff; }
        .tagline { text-align: center; font-size: 16px; font-style: italic; color: #b0bec5; }
        </style>
        """,
        unsafe_allow_html=True,
    )
