from pathlib import Path
from fastapi import APIRouter, HTTPException
from document_processing.document_service import process_document
from extraction.requirement_extractor import extract_requirements
from extraction.supplier_extractor import extract_supplier_from_text

router = APIRouter(prefix="/api")

@router.post("/extract/{filename}")
async def extract_document_data(filename: str):
    file_path = Path("uploads") / Path(filename).name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        # 1. Process document into raw evidence
        evidence = process_document(file_path)

        # 2. Extract structured requirements
        requirements = extract_requirements(evidence)

        # 3. Extract structured supplier profile
        supplier = extract_supplier_from_text(evidence)

        # 4. Return structured data
        return {
            "filename": filename,
            "evidence_count": len(evidence),
            "requirements": [req.__dict__ for req in requirements],
            "supplier": supplier.__dict__ if supplier else None
        }

    except Exception as error:
        raise HTTPException(
            status_code=500, 
            detail=f"Extraction failed: {error}"
        )