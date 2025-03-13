import streamlit as st

def render_sidebar():
    """Render sidebar with settings and user options"""
    with st.sidebar:
        st.title("⚙️ Settings")
        st.write("Customize your chat experience.")
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
