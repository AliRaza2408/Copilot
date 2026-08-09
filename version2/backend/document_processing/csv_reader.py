from pathlib import Path
import pandas as pd

def read_csv(file_path: str | Path) -> list[dict]:
    """
    Read a CSV file and return row-level evidence.
    """
    file_path = Path(file_path)
    dataframe = pd.read_csv(file_path)
    dataframe = dataframe.fillna("")
    results = []

    for row_number, row in dataframe.iterrows():
        results.append({
            "source": file_path.name,
            "file_type": "csv",
            "row": row_number + 2,
            "data": row.to_dict()
        })

    return results