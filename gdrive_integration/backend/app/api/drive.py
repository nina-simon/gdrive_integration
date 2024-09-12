from fastapi import APIRouter, Request, UploadFile, HTTPException
from app.utils.drive_helpers import upload_to_drive, download_from_drive, delete_from_drive, list_drive_files

router = APIRouter()

# Upload API
@router.post("/upload")
async def upload_file(request: Request, file: UploadFile):
    return await upload_to_drive(request, file)

# Download API
@router.get("/download/{file_id}")
async def download_file(request: Request, file_id: str):
    return await download_from_drive(request, file_id)

# Delete API
@router.delete("/delete/{file_id}")
async def delete_file(request: Request, file_id: str):
    return await delete_from_drive(request, file_id)

# List Files API
@router.get("/list")
async def list_files(request: Request):
    return await list_drive_files(request)
