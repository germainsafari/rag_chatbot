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
# Custom CSS for dark mode
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        * {
            font-family: 'Roboto', sans-serif;
        }

        /* Main container styling with padding and centering */
        .main {
            padding: 2rem; 
            max-width: 1200px; 
            margin: 0 auto; 
        }

        /* Apply padding to the body */
        .css-1y4p8pa {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        /* Header and navigation styling */
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background-color: #1e1e1e; /* Dark background */
            border-bottom: 1px solid #444; /* Darker border */
        }
        
        /* Centered greeting and question styling */
        .centered-greeting {
            text-align: center;
            font-size: 48px;
            font-weight: 700;
            margin-top: 4rem;
            color: #ffffff; /* White text for dark mode */
        }
        
        .subheading {
            text-align: center;
            font-size: 32px;
            font-weight: 300;
            color: #bbbbbb; /* Light grey for contrast */
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
        
        /* Quick prompt grid styling */
        .quick-prompt-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .quick-prompt {
            background-color: #333333; /* Dark grey for quick prompts */
            border: 1px solid #555555; /* Dark border */
            border-radius: 12px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
            color: #ffffff; /* White text */
        }
        
        .quick-prompt:hover {
            background-color: #444444; /* Slightly lighter on hover */
            transform: translateY(-2px);
        }
        
        /* Chat message styling */
        .chat-container {
            margin-top: 2rem;
            border-radius: 12px;
            background-color: #1e1e1e; /* Dark background for chat */
        }
        
        .chat-message {
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: #ffffff; /* White text */
        }
        
        .chat-message.user {
            background-color: #333333; /* User message background */
        }
        
        .chat-message.assistant {
            background-color: #444444; /* Assistant message background */
        }
        
        /* Input box styling */
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #1e1e1e; /* Dark input background */
            padding: 1rem 2rem;
            border-top: 1px solid #444444; /* Darker border */
        }
        
        .stTextInput>div>div>textarea {
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #555555; /* Dark border */
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            resize: none;
            background-color: #333333; /* Dark background for input */
            color: #ffffff; /* White text */
        }
        
        .stTextInput>div>div>textarea:focus {
            border-color: #7749F8;
            box-shadow: none;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            padding: 1rem;
            color: #bbbbbb; /* Light grey text */
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