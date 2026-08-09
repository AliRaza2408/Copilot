from pathlib import Path
from docx import Document

def read_docx(file_path: str | Path) -> list[dict]:
    """
    Read a DOCX document and return paragraph-level evidence.
    """
    file_path = Path(file_path)
    document = Document(file_path)
    results = []

    for paragraph_number, paragraph in enumerate(document.paragraphs, start=1):
        text = paragraph.text.strip()
        if not text:
            continue
            
        results.append({
            "source": file_path.name,
            "file_type": "docx",
            "paragraph": paragraph_number,
            "text": text
        })

    return results