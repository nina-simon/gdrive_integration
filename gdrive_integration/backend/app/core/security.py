from fastapi import Request, HTTPException
from google_auth_oauthlib.flow import Flow
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from app.core.config import settings

def authenticate_user(request: Request):
    try:
        flow = Flow.from_client_secrets_file(settings.GOOGLE_CREDENTIALS_PATH, scopes=settings.GOOGLE_SCOPES)
        flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        request.session['state'] = state
        return {"url": authorization_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

async def oauth_callback(request: Request):
    try:
        state = request.query_params.get('state')
        code = request.query_params.get('code')
        
        print(f"Debug: Received state: {state}")
        print(f"Debug: Received code: {code}")
        
        flow = Flow.from_client_secrets_file(settings.GOOGLE_CREDENTIALS_PATH, scopes=settings.GOOGLE_SCOPES, 
                                             state=state)
        flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
        
        print(f"Debug: Flow redirect_uri: {flow.redirect_uri}")
        
        flow.fetch_token(code=code)
        credentials = flow.credentials

        request.session['credentials'] = credentials_to_dict(credentials)
        
        print("Debug: Successfully fetched token and stored credentials")
        
        return RedirectResponse(url=f"{settings.FRONTEND_REDIRECT_URI}?success=true")
    except Exception as e:
        print(f"Debug: Error in oauth2callback: {str(e)}")
        return RedirectResponse(url=f"{settings.FRONTEND_REDIRECT_URI}?error={str(e)}")

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
