"""
Configuration settings for TalentScout Hiring Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

# Conversation settings
MAX_CONVERSATION_TURNS = 50
END_KEYWORDS = ["goodbye", "bye", "exit", "quit", "end", "stop", "thank you", "thanks"]

# Required candidate information
REQUIRED_INFO = [
    "full_name",
    "email",
    "phone",
    "experience_years",
    "desired_position",
    "location",
    "tech_stack"
]

# UI Configuration
PAGE_TITLE = "TalentScout Hiring Assistant"
PAGE_ICON = "🤖"
