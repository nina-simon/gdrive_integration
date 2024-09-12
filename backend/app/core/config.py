import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_SCOPES=os.getenv("GOOGLE_SCOPES")
    GOOGLE_REDIRECT_URI=os.getenv("GOOGLE_REDIRECT_URI")
    GOOGLE_CREDENTIALS_PATH=os.getenv("GOOGLE_CREDENTIALS_PATH") 
    FRONTEND_REDIRECT_URI=os.getenv("FRONTEND_REDIRECT_URI")
    SESSION_SECRET_KEY=os.getenv("SESSION_SECRET_KEY")
    FRONTEND_URI=os.getenv("FRONTEND_URI")
    GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
    GOOGLE_DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"

settings = Settings()
