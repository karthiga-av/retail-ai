from fastapi import APIRouter, UploadFile, File
import shutil
import os
from app.services.ingestion_service import ingest

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return ingest(file_path)