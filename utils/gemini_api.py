import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Read API Key
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_response(prompt):
    """
    Generates a response using Gemini AI.
    If Gemini fails, returns None.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return None