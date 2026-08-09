import os
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool  # <-- ADD THIS IMPORT
from services.decision_service import DecisionService

router = APIRouter(prefix="/api/decision", tags=["Decision"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/process")
async def process_decision(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    saved_paths = []

    for file in files:
        safe_prefix = uuid.uuid4().hex[:8]
        safe_filename = f"{safe_prefix}_{file.filename.replace(' ', '_').lower()}"
        file_path = UPLOAD_DIR / safe_filename

        contents = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        
        saved_paths.append(file_path)

    service = DecisionService()
    
    # Run the heavy synchronous LLM pipeline in a threadpool so it doesn't freeze the server
    result = await run_in_threadpool(service.process_case, saved_paths)
    
    return result