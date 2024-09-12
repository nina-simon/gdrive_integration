from fastapi import UploadFile, Request, HTTPException
from fastapi.responses import StreamingResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload


async def get_credentials(request: Request):
    credentials_dict = request.session.get('credentials')
    if not credentials_dict:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials_dict

# Upload File Helper
async def upload_to_drive(request: Request, file: UploadFile):
    print(f"Get upload call")
    credentials_dict = await get_credentials(request)
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


# Download File Helper
async def download_from_drive(request: Request, file_id: str):
    print(f"Get doownload call")
    credentials_dict = await get_credentials(request)
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


# Delete File Helper
async def delete_from_drive(request: Request, file_id: str):
    print(f"Delete call for file: {file_id}")
    credentials_dict = await get_credentials(request)
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

# List Files Helper
async def list_drive_files(request: Request):
    print(f"Get list call")
    credentials_dict = await get_credentials(request)
    # Deserialize the credentials dictionary to Credentials object
    credentials = Credentials(**credentials_dict)

    try:
        service = build('drive', 'v3', credentials=credentials)
        results = service.files().list(pageSize=10).execute()
        items = results.get('files', [])
        print(f"Debug: {items}")
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))