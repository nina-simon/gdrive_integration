# Google Drive Integration Web Application

## Overview
This project is a web-based application that integrates with Google Drive to allow users to authenticate, upload, download, delete, and list files. The project is divided into two main parts:

- **Backend**: A FastAPI-based server that handles Google OAuth2 authentication and interacts with Google Drive for file operations.
- **Frontend**: A React-based user interface that interacts with the backend to perform file operations and handle user interactions.

## Project Structure

```bash
.
├── backend                  # FastAPI Backend
│   ├── app                  # FastAPI core application directory
│   ├── main.py              # FastAPI entry point
│   ├── requirements.txt     # Python dependencies
│   ├── client_secret.json   # Google OAuth credentials (ensure security)
│   ├── .env                 # Environment variables for backend
|   └── README.md            # Backend-specific setup instructions
├── frontend                 # React Frontend
│   ├── public               # Public assets
│   ├── src                  # React components and logic
│   ├── package.json         # Frontend dependencies
│   └── README.md            # Frontend-specific setup instructions
└── README.md                # Project-wide readme (this file)
```

## Features

### Backend (FastAPI)
- Google OAuth2 integration for authentication
- File operations with Google Drive:
    - Upload files
    - Download files
    - Delete files
    - List files
### Frontend (React)
- User-friendly interface for interacting with Google Drive
- Displays files in a list with options to upload, download, and delete
- Handles OAuth2 flow for Google authentication

## How to Use
- Clone the repository and follow the setup instructions in the respective directories (backend/README.md and frontend/README.md).
- Configure the environment variables in the .env file and set up your Google Cloud Project for OAuth.

## Loom Video - Developing a Google Drive Integration Application

https://www.loom.com/share/dac28f9924704196a2a63fd7b798cf52
