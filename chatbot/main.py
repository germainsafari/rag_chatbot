import streamlit as st
from rag_function import rag
import time
from datetime import datetime

# --- Initial Setup and Styles ---
st.set_page_config(
    page_title="Mura - Your AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        * {
            font-family: 'Roboto', sans-serif;
        }

        #MainMenu {visibility: hidden;}

        .main {
            padding: 2rem; 
            max-width: 1200px; 
            margin: 0 auto; 
        }

        .css-1y4p8pa {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background-color: #1e1e1e;
            border-bottom: 1px solid #444;
        }
        
        .centered-greeting {
            text-align: center;
            font-size: 48px;
            font-weight: 700;
            margin-top: 4rem;
            color: #ffffff;
        }
        
        .subheading {
            text-align: center;
            font-size: 32px;
            font-weight: 300;
            color: #bbbbbb;
            margin-top: 1rem;
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
        
        .quick-prompt-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .quick-prompt {
            background-color: #333333;
            border: 1px solid #555555;
            border-radius: 12px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 200px;
            flex-grow: 1;
            height: 200px;
        }
        
        .quick-prompt:hover {
            background-color: #444444;
            transform: translateY(-2px);
        }
        
        .chat-container {
            margin-top: 2rem;
            border-radius: 12px;
            background-color: #1e1e1e;
        }
        
        .chat-message {
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: #ffffff;
        }
        
        .chat-message.user {
            background-color: #333333;
        }
        
        .chat-message.assistant {
            background-color: #444444;
        }
        
        .input-box {
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #555555;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            resize: none;
            background-color: #333333;
            color: #ffffff;
            width: 80%;
            margin-right: 1rem;
        }
        
        .send-button {
            background-color: #7749F8;
            color: white;
            border-radius: 12px;
            border: none;
            padding: 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
            width: 18%;
        }
        
        .send-button:hover {
            background-color: #6040D8;
        }

        .footer {
            text-align: center;
            padding: 1rem;
            color: #bbbbbb;
            font-size: 14px;
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

# Message Input with Enter functionality
with st.container():
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    user_input = st.text_area("", key="user_input", height=100, placeholder="Type your message...")
    if st.button("Send", key="send_button", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = rag(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class='footer'>
        Mura by Carl. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True
)
