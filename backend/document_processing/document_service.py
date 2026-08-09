from pathlib import Path
from .pdf_reader import read_pdf
from .excel_reader import read_excel
from .docx_reader import read_docx
from .csv_reader import read_csv
from .txt_reader import read_txt  # <-- ADD THIS IMPORT

SUPPORTED_EXTENSIONS = {".pdf", ".xlsx", ".xls", ".docx", ".csv", ".txt"}  # <-- ADD .txt

def evidence_to_text(item: dict) -> str:
    """Extract searchable text from an evidence item, handling both
    text-based (PDF/DOCX/TXT) and tabular (CSV/XLSX) readers."""
    text = item.get("text")
    if text:
        return str(text)
    data = item.get("data")
    if isinstance(data, dict):
        return "\n".join(f"{key}: {value}" for key, value in data.items() if value)
    if data is not None:
        return str(data)
    return ""

def _normalize_evidence(item: dict) -> dict:
    """Ensure every evidence item exposes a `text` field so downstream
    services (RAG, extraction, decision engine) can rely on it."""
    item = dict(item)
    if "text" not in item:
        item["text"] = evidence_to_text(item)
    return item

def process_document(file_path: str | Path) -> list[dict]:
    """
    Automatically select the correct reader based on the file extension.
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return [_normalize_evidence(item) for item in read_pdf(file_path)]
    if extension in {".xlsx", ".xls"}:
        return [_normalize_evidence(item) for item in read_excel(file_path)]
    if extension == ".docx":
        return [_normalize_evidence(item) for item in read_docx(file_path)]
    if extension == ".csv":
        return [_normalize_evidence(item) for item in read_csv(file_path)]
    if extension == ".txt":           # <-- ADD THIS BLOCK
        return [_normalize_evidence(item) for item in read_txt(file_path)]

    raise ValueError(f"Unsupported document type: {extension}")