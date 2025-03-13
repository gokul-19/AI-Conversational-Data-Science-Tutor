import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv 

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY") or st.secrets["google"]["api_key"]

# Apply background image using CSS
def add_bg_from_local(image_file):
    """Sets a background image for the Streamlit app."""
    bg_style = f"""
    <style>
    .stApp {{
        background: url("{image_file}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# Initialize memory
memory = ConversationBufferMemory()

# Initialize AI Model
chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key=google_api_key)

def conversational_tutor(user_input):
    """Processes user input and generates AI response."""
    memory.save_context({"human": user_input}, {"ai": "Processing..."})  
    conversation_history = memory.load_memory_variables({})
    
    prompt = f"""
    You are a data science tutor. Answer ONLY data science-related questions.
    If the user asks something unrelated, politely decline.
    Keep the conversation aware using memory.

    Conversation history: {conversation_history}

    User: {user_input}
    """
    
    response = chat_model.invoke(prompt)
    response_text = response.content if hasattr(response, 'content') else str(response)

    memory.save_context({"human": user_input}, {"ai": response_text})  
    return response_text

# Streamlit UI
def main():
    st.set_page_config(page_title="Data Science Tutor", page_icon="📊", layout="wide")

    # Add background image
    add_bg_from_local("static/img/background.jpg")

    st.title("Conversational AI Data Science Tutor")
    st.write("Ask me anything about Data Science!")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        response = conversational_tutor(user_input)
        st.session_state["messages"].append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()
