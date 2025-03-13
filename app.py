import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import time
import base64

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY") or st.secrets["google"]["api_key"]

# Initialize memory
memory = ConversationBufferMemory()

# Initialize Gemini 1.5 Pro Model
chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key=google_api_key)

# Function to add background image
def add_bg_from_local(image_file):
    """Sets a background image using local file."""
    with open(image_file, "rb") as image:
        img_bytes = base64.b64encode(image.read()).decode()
    bg_style = f"""
    <style>
    .stApp {{
        background: url("data:image/jpeg;base64,{img_bytes}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# Call function to set background
add_bg_from_local("static/img/background.jpg")

def conversational_tutor(user_input):
    """Function to interact with the conversational AI tutor."""
    memory.save_context({"human": user_input}, {"ai": "Processing..."})  # Temporary response
    
    conversation_history = memory.load_memory_variables({})
    
    prompt = f"""
    You are a data science tutor. Answer ONLY data science-related questions.
    If the user asks something unrelated, politely decline.
    Keep the conversation aware using memory.
    
    Conversation history: {conversation_history}
    
    User: {user_input}
    """
    
    response = chat_model.invoke(prompt)
    
    # Extract content properly
    if hasattr(response, 'content'):
        response_text = response.content
    elif isinstance(response, dict):
        response_text = response.get("content", "I'm sorry, I couldn't generate a response.")
    else:
        response_text = str(response)

    # Store cleaned response in memory
    memory.save_context({"human": user_input}, {"ai": response_text})

    return response_text

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Data Science Tutor AI",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Conversational AI Data Science Tutor")
    st.write("Ask me anything about Data Science!")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Type your question here...")  # Prevents duplicate element errors

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        response = conversational_tutor(user_input)
        st.session_state["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()
