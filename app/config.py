import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Try Streamlit Cloud Secrets first
try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
except Exception:
    GROQ_API_KEY = None

# Fall back to .env when running locally
if not GROQ_API_KEY:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not configured.")