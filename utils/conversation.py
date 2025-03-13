import os
from dotenv import load_dotenv

# Load API key from environment
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")

class DataScienceTutor:
    def __init__(self):
        if not API_KEY:
            raise ValueError("Missing API Key! Please set 'GENAI_API_KEY' in your .env file.")

    def get_response(self, user_message):
        """Mock response generator (Replace this with actual API call)"""
        return f"🤖 AI: You asked - '{user_message}'. Here's some insight..."
