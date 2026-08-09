from pathlib import Path

def read_txt(file_path: str | Path) -> list[dict]:
    """
    Read a plain text file and return it as a single evidence item.
    """
    file_path = Path(file_path)
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        return []

    return [{
        "source": file_path.name,
        "file_type": "txt",
        "page": 1,  # Text files don't have pages, so we default to 1
        "text": text
    }]