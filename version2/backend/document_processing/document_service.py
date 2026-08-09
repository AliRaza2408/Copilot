from pathlib import Path
from .pdf_reader import read_pdf
from .excel_reader import read_excel
from .docx_reader import read_docx
from .csv_reader import read_csv
from .txt_reader import read_txt  # <-- ADD THIS IMPORT

SUPPORTED_EXTENSIONS = {".pdf", ".xlsx", ".xls", ".docx", ".csv", ".txt"}  # <-- ADD .txt

def process_document(file_path: str | Path) -> list[dict]:
    """
    Automatically select the correct reader based on the file extension.
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return read_pdf(file_path)
    if extension in {".xlsx", ".xls"}:
        return read_excel(file_path)
    if extension == ".docx":
        return read_docx(file_path)
    if extension == ".csv":
        return read_csv(file_path)
    if extension == ".txt":           # <-- ADD THIS BLOCK
        return read_txt(file_path)

    raise ValueError(f"Unsupported document type: {extension}")