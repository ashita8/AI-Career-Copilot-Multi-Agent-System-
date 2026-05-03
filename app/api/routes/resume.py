from fastapi import APIRouter, UploadFile, File, Form
import os
import uuid

from services.pdf_parser import extract_text_from_pdf
from graph.builder import graph

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    message: str = Form("")
):
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.pdf"

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_text_from_pdf(file_path)

        if message.strip():

            thread_id = str(uuid.uuid4())

            config = {
                "configurable": {
                    "thread_id": thread_id
                }
            }

            result = graph.invoke(
                {
                    "message": message,
                    "resume_text": text
                },
                config=config
            )

            return {
                "thread_id": thread_id,
                "result": result
            }

        return {
            "resume_text_preview": text
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)