import streamlit as st
import google.generativeai as genai

# Read API key from Streamlit Secrets
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_response(prompt):
    """
    Generates a response using Gemini AI.
    Returns None if Gemini fails.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return None