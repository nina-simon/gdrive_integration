from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api import auth, drive
from app.core.config import settings
import os

# Allow OAuth2 flow to use HTTP (only for development)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Create FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from frontend (e.g., React on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Session middleware for storing session data (e.g., credentials)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)  # Use a strong secret key in production

# Include routes from the auth and drive modules
app.include_router(auth.router, prefix="/auth")
app.include_router(drive.router, prefix="/drive")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Google Drive Integration API"}
