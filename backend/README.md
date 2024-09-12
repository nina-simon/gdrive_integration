# Google Drive Integration - FastAPI Backend

## Overview
This FastAPI backend integrates with Google Drive to provide file upload, download, delete, and listing functionality. It also supports OAuth2 for Google authentication.

## Setup
### Prerequisites
- Python 3.9+
- Google Cloud Project with OAuth credentials (Download client_secret.json from Google Console)
- virtualenv or similar tool for creating a virtual environment

## Environment Variables
Create a .env file in the backend root directory and add the following:

```bash
CLIENT_SECRETS_FILE=client_secret.json
SCOPES=https://www.googleapis.com/auth/drive
REDIRECT_URI=http://localhost:8000/oauth2callback
CORS_ORIGIN=http://localhost:3000
SESSION_SECRET_KEY=your_secret_key

```
## Install Dependencies
Create a virtual environment and install the required packages:
``` bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

## Run the Server
```bash
uvicorn main:app --reload
```

## Directory Structure
```bash
.
├── app
│   ├── api                # Holds all the API routes
│   ├── services           # Business logic for Google Drive
│   ├── utils              # Helper functions (e.g., Google API wrappers)
│   └── __init__.py        # App initialization and configuration
|   └── main.py                # FastAPI app initialization
├── .env                   # Environment variables file
├── client_secret.json      # Google OAuth credentials (secure this file)
└── requirements.txt       # Python dependencies
```

## API Endpoints
### Authentication
- GET /auth - Initiates Google OAuth flow
- GET /oauth2callback - Callback to handle OAuth response
### File Operations
- POST /upload - Upload a file to Google Drive
- GET /list - List files from Google Drive
- GET /download/{file_id} - Download a file from Google Drive
- DELETE /delete/{file_id} - Delete a file from Google Drive

### Middleware
The app uses:
**CORSMiddleware:** For handling Cross-Origin Resource Sharing
**SessionMiddleware:** For managing session data