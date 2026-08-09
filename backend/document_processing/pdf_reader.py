from pathlib import Path
import pymupdf

def read_pdf(file_path: str | Path) -> list[dict]:
    file_path = Path(file_path)
    document = pymupdf.open(file_path)
    results = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()
        
        # REAL-WORLD CHECK: Detect Scanned PDFs
        if not text:
            results.append({
                "source": file_path.name,
                "file_type": "pdf",
                "page": page_number,
                "text": "No selectable text found. Document appears to be scanned or image-based. OCR fallback required.",
                "is_scanned": True # Flag for the reliability layer
            })
            continue
        
        text = text.replace('\n', ' ').replace('  ', ' ')
        
        results.append({
            "source": file_path.name,
            "file_type": "pdf",
            "page": page_number,
            "text": text,
            "is_scanned": False
        })

    document.close()
    return results