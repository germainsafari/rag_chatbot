import streamlit as st
from rag_function import rag
import time
from datetime import datetime

# --- Initial Setup and Styles ---
st.set_page_config(
    page_title="Mura - Your AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        * {
            font-family: 'Roboto', sans-serif;
        }
        
        /* Main container styling */
        .main {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Header and navigation styling */
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background-color: white;
            border-bottom: 1px solid #eee;
        }
        
        /* Centered greeting and question styling */
        .centered-greeting {
            text-align: center;
            font-size: 48px;
            font-weight: 700;
            margin-top: 4rem;
            color: #1a1a1a;
            font-family: 'Roboto', sans-serif;
        }
        
        .subheading {
            text-align: center;
            font-size: 32px;
            font-weight: 300;
            color: #666;
            margin-top: 1rem;
            font-family: 'Roboto', sans-serif;
        }
        
        .guidelines-link {
            text-align: center;
            margin-top: 1rem;
            font-size: 16px;
        }
        
        .guidelines-link a {
            color: #7749F8;
            text-decoration: none;
        }
        
        /* Quick prompt grid styling */
        .quick-prompt-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .quick-prompt {
            background-color: #F8F9FA;
            border: 1px solid #E9ECEF;
            border-radius: 12px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
            color: #1a1a1a;
            font-family: 'Roboto', sans-serif;
        }
        
        .quick-prompt:hover {
            background-color: #F1F3F5;
            transform: translateY(-2px);
        }
        
        /* Chat message styling */
        .chat-container {
            margin-top: 2rem;
            border-radius: 12px;
            background-color: white;
        }
        
        .chat-message {
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            font-family: 'Roboto', sans-serif;
        }
        
        .chat-message.user {
            background-color: #F8F9FA;
        }
        
        .chat-message.assistant {
            background-color: #F8F9FA;
        }
        
        /* Input box styling */
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            padding: 1rem 2rem;
            border-top: 1px solid #eee;
        }
        
        .stTextInput>div>div>textarea {
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #E9ECEF;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            resize: none;
            background-color: #F8F9FA;
        }
        
        .stTextInput>div>div>textarea:focus {
            border-color: #7749F8;
            box-shadow: none;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            padding: 1rem;
            color: #666;
            font-size: 14px;
            font-family: 'Roboto', sans-serif;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for messages if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

# Centered Greeting
st.markdown("<div class='centered-greeting'>Hello, Carl</div>", unsafe_allow_html=True)
st.markdown("<div class='subheading'>How can I help you today?</div>", unsafe_allow_html=True)
st.markdown("<div class='guidelines-link'><a href='#'>Click to know mura guidelines ↗</a></div>", unsafe_allow_html=True)

# Quick Prompts in a Grid Layout
quick_prompts = [
    "I have a depression, got divorced last year I can't put my things together",
    "Help me quit smoking",
    "Give me some recommendations for ADHD disorder",
    "I experienced trauma as a child, could you run a therapy session for me?"
]

# Create a container for the quick prompts grid
st.markdown("<div class='quick-prompt-grid'>", unsafe_allow_html=True)
cols = st.columns(4)
for idx, (col, prompt) in enumerate(zip(cols, quick_prompts)):
    with col:
        if st.button(prompt, key=f"quick_prompt_{idx}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = rag(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
st.markdown("</div>", unsafe_allow_html=True)

# Chat Messages Container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "assistant"
    icon = "👤" if message["role"] == "user" else "🤖"
    name = "You" if message["role"] == "user" else "Mura"
    st.markdown(
        f"<div class='chat-message {role_class}'>{icon} <strong>{name}:</strong> {message['content']}</div>",
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# Message Input
with st.container():
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    user_input = st.text_area("Message", key="user_input", height=100)
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Send", use_container_width=True) and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                response = rag(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class='footer'>
        Mura may display inaccurate info, so double-check its responses.
    </div>
    """,
    unsafe_allow_html=True
)