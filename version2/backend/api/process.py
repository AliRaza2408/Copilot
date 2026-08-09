from pathlib import Path
from fastapi import APIRouter, HTTPException
from document_processing.document_service import process_document

router = APIRouter(prefix="/api")

@router.post("/process/{filename}")
async def process_uploaded_document(filename: str):
    # Security: ensure we only look inside the uploads directory
    file_path = Path("uploads") / Path(filename).name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        evidence = process_document(file_path)
        return {
            "filename": filename,
            "evidence_count": len(evidence),
            "evidence": evidence
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {error}")