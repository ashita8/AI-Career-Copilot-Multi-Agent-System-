from fastapi import APIRouter, UploadFile, File
import os
import uuid

from app.services.pdf_parser import extract_text_from_pdf
from app.graph.builder import graph

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.pdf"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)

    return {
        "file_id": file_id,
        "resume_text_preview": text[:1500]
    }