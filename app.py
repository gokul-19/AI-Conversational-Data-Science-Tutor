import streamlit as st
from utils.conversation import DataScienceTutor
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    defaults = {
        "tutor": DataScienceTutor(),
        "messages": [],
        "chat_history": [],
        "thinking": False,
        "header_rendered": False
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

def load_custom_css():
    """Load and apply custom CSS"""
    try:
        with open("static/css/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Style file not found. UI may not display properly.")

def main():
    st.set_page_config(
        page_title="Data Science Tutor AI",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={'About': "Data Science Tutor AI powered by Gemini 1.5 Pro"}
    )

    # Load custom styles
    load_custom_css()

    # Initialize session state
    initialize_session_state()

    # Only render the title if not processing a response
    if not st.session_state.thinking:
        col1, col2 = st.columns([1, 9])
        with col1:
            try:
                st.image("static/img/logo.svg", width=80)
            except FileNotFoundError:
                st.warning("⚠️ Logo file not found.")
        with col2:
            st.markdown('<h1 class="main-title">Data Science Tutor AI</h1>', unsafe_allow_html=True)
            st.markdown('<h3 class="subtitle">Your personal AI assistant for data science learning</h3>', unsafe_allow_html=True)
        st.session_state.header_rendered = True

    # Render sidebar
    render_sidebar()

    # Render chat interface
    render_chat_interface()

    # Process assistant response
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and not st.session_state.thinking:
        st.session_state.thinking = True

        user_message = st.session_state.messages[-1]["content"]

        with st.chat_message("assistant", avatar="static/img/logo.svg"):
            message_placeholder = st.empty()
            message_placeholder.markdown('<div class="message assistant-message">Thinking...</div>', unsafe_allow_html=True)

            try:
                response = st.session_state.tutor.get_response(user_message)
                displayed_response = ""
                
                # Stream response dynamically
                for chunk in response.split():
                    displayed_response += chunk + " "
                    message_placeholder.markdown(f'<div class="message assistant-message">{displayed_response}▌</div>', unsafe_allow_html=True)
                    time.sleep(0.01)

                # Display final response
                message_placeholder.markdown(f'<div class="message assistant-message">{response}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            except Exception as e:
                error_message = f"Sorry, I encountered an error: {str(e)}"
                message_placeholder.markdown(f'<div class="message assistant-message">{error_message}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

        st.session_state.thinking = False
        st.session_state.header_rendered = False
        st.rerun()

if __name__ == "__main__":
    main()
