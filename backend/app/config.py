import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "Cura"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cura.db")

    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


settings = Settings()