from fastapi import APIRouter, Request
from app.core.security import authenticate_user, oauth_callback

router = APIRouter()

# Authentication API
@router.get("/login")
async def login(request: Request):
    return authenticate_user(request)

@router.get("/oauth2callback")
async def oauth_callback_handler(request: Request):
    return await oauth_callback(request)
