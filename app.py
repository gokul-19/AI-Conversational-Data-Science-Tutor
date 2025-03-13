import os
import streamlit as st
from utils.conversation import DataScienceTutor
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "tutor" not in st.session_state:
        st.session_state.tutor = DataScienceTutor()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "thinking" not in st.session_state:
        st.session_state.thinking = False
    if "header_rendered" not in st.session_state:
        st.session_state.header_rendered = False

def main():
    st.set_page_config(
        page_title="Data Science Tutor AI",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Data Science Tutor AI powered by Gemini 1.5 Pro"
        }
    )

    # Apply custom CSS before any elements are rendered
    css_path = "static/css/style.css"
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Style file not found. UI may not display properly.")

    # Initialize session state
    initialize_session_state()

    # Load and display logo
    logo_path = "static/img/logo.png"
    if os.path.exists(logo_path):
        col1, col2 = st.columns([1, 9])
        with col1:
            st.image(logo_path, width=80)
        with col2:
            st.markdown('<h1 class="main-title">Data Science Tutor AI</h1>', unsafe_allow_html=True)
            st.markdown('<h3 class="subtitle">Your personal AI assistant for data science learning</h3>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Logo file not found.")

    # Render sidebar with options
    render_sidebar()

    # Render main chat interface
    render_chat_interface()

    # Process assistant response
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and not st.session_state.thinking:
        st.session_state.thinking = True

        user_message = st.session_state.messages[-1]["content"]

        with st.chat_message("assistant", avatar=logo_path):
            message_placeholder = st.empty()
            message_placeholder.markdown('<div class="message assistant-message">Thinking...</div>', unsafe_allow_html=True)

            try:
                response = st.session_state.tutor.get_response(user_message)

                displayed_response = ""
                for chunk in response.split():
                    displayed_response += chunk + " "
                    message_placeholder.markdown(
                        f'<div class="message assistant-message">{displayed_response}▌</div>', 
                        unsafe_allow_html=True
                    )
                    time.sleep(0.01)

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
