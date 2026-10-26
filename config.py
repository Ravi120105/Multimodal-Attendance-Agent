import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "attendance_agent.db"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
APP_TITLE = "Multimodal Attendance & Engagement Agent"
VERSION = "1.0.0"