from pathlib import Path
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter(prefix="/api")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".xlsx", ".xls", ".csv", ".docx", ".txt"}

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        if not file.filename:
            continue

        extension = Path(file.filename).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {extension}"
            )

        # Generate safe filename
        safe_prefix = uuid.uuid4().hex[:8]
        safe_filename = f"{safe_prefix}_{Path(file.filename).name}"
        file_path = UPLOAD_DIR / safe_filename

        contents = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        uploaded_files.append({
            "filename": file.filename,
            "size": len(contents),
            "type": extension,
            "status": "uploaded"
        })

    return {
        "message": "Files uploaded successfully",
        "files": uploaded_files
    }