# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key and database path
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
DATABASE_PATH = "financial_data.db"