import streamlit as st

def render_chat_interface():
    """Render chat messages"""
    for message in st.session_state.messages:
        role, content = message["role"], message["content"]
        avatar = "static/img/logo.svg" if role == "assistant" else None
        with st.chat_message(role, avatar=avatar):
            st.markdown(content, unsafe_allow_html=True)
    
    if user_input := st.chat_input("Ask me about Data Science!"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
