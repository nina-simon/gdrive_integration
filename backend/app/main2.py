import os
from fastapi import FastAPI, UploadFile, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from starlette.middleware.sessions import SessionMiddleware
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="123456qwerty")

# Allow OAuth2 flow to use HTTP (only for development)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRETS_FILE = "./app/client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/drive']
REDIRECT_URI = "http://localhost:8000/oauth2callback"  # Change this back to backend URL
FRONTEND_REDIRECT_URL = "http://localhost:3000/oauth2callback"  # Add this for frontend redirect

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

@app.get("/auth")
async def auth(request: Request):
    try:
        flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
        flow.redirect_uri = REDIRECT_URI
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        request.session['state'] = state
        return {"url": authorization_url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/oauth2callback")
async def oauth2callback(request: Request):
    try:
        state = request.query_params.get('state')
        code = request.query_params.get('code')
        
        print(f"Debug: Received state: {state}")
        print(f"Debug: Received code: {code}")
        
        flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
        flow.redirect_uri = REDIRECT_URI
        
        print(f"Debug: Flow redirect_uri: {flow.redirect_uri}")
        
        flow.fetch_token(code=code)
        credentials = flow.credentials

        request.session['credentials'] = credentials_to_dict(credentials)
        
        print("Debug: Successfully fetched token and stored credentials")
        
        return RedirectResponse(url=f"{FRONTEND_REDIRECT_URL}?success=true")
    except Exception as e:
        print(f"Debug: Error in oauth2callback: {str(e)}")
        return RedirectResponse(url=f"{FRONTEND_REDIRECT_URL}?error={str(e)}")

# API to list Google Drive files using credentials from session
@app.get("/list")
async def list_files(request: Request):
    print(f"Get list call")
    credentials_dict = request.session.get('credentials')
    # Deserialize the credentials dictionary to Credentials object
    credentials = Credentials(
            token=credentials_dict.get('token'),
            refresh_token=credentials_dict.get('refresh_token'),
            token_uri=credentials_dict.get('token_uri'),
            client_id=credentials_dict.get('client_id'),
            client_secret=credentials_dict.get('client_secret'),
            scopes=credentials_dict.get('scopes')
        )
    try:
        service = build('drive', 'v3', credentials=credentials)
        results = service.files().list(pageSize=10).execute()
        items = results.get('files', [])
        print(f"Debug: {items}")
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API to upload a file to Google Drive
@app.post("/upload")
async def upload_file(request: Request, file: UploadFile):
    print(f"Get upload call")
    credentials_dict = request.session.get('credentials')
    
    # Deserialize the credentials dictionary to Credentials object
    credentials = Credentials(**credentials_dict)
    
    try:
        service = build('drive', 'v3', credentials=credentials)
        
        # Read file content into BytesIO
        file_content = await file.read()  # Read the file's content
        file_metadata = {'name': file.filename}

        # Use BytesIO for the media body
        media = MediaIoBaseUpload(BytesIO(file_content), mimetype=file.content_type)

        # Upload the file to Google Drive
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return {"file_id": uploaded_file.get("id")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# API to download a file from Google Drive
@app.get("/download/{file_id}")
async def download_file(request: Request, file_id: str):
    print(f"Get doownload call")
    credentials_dict = request.session.get('credentials')
    # Deserialize the credentials dictionary to Credentials object
    credentials = Credentials(**credentials_dict)
    print(f"Debug: {file_id}")
    try:
        service = build('drive', 'v3', credentials=credentials)
        request = service.files().get_media(fileId=file_id)
        file_io = BytesIO()
        downloader = MediaIoBaseDownload(file_io, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        file_io.seek(0)  # Move to the beginning of the BytesIO stream
        # Return the file as a response
        return StreamingResponse(file_io, media_type='application/octet-stream', headers={"Content-Disposition": f"attachment; filename={file_id}.file"})

    except Exception as e:
        raise HTTPException(status_code = 500, detail=f"File download failed: {str(e)}")



# API to delete a file from Google Drive
@app.delete("/delete/{file_id}")
async def delete_file(request: Request, file_id: str):
    print(f"Delete call for file: {file_id}")
    credentials_dict = request.session.get('credentials')

    # Deserialize the credentials dictionary to Credentials object
    credentials = Credentials(**credentials_dict)

    try:
        # Initialize the Google Drive service
        service = build('drive', 'v3', credentials=credentials)

        # Call the delete method to remove the file
        service.files().delete(fileId=file_id).execute()

        return {"message": f"File {file_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)