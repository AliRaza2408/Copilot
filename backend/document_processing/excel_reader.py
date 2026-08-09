from pathlib import Path
import pandas as pd

def read_excel(file_path: str | Path) -> list[dict]:
    """
    Read all sheets from an Excel workbook and return row-level evidence.
    """
    file_path = Path(file_path)
    workbook = pd.ExcelFile(file_path)
    results = []

    for sheet_name in workbook.sheet_names:
        dataframe = pd.read_excel(file_path, sheet_name=sheet_name)
        dataframe = dataframe.fillna("")

        for row_number, row in dataframe.iterrows():
            row_data = row.to_dict()
            results.append({
                "source": file_path.name,
                "file_type": "excel",
                "sheet": sheet_name,
                "row": row_number + 2, # +2 because Excel is 1-indexed and has a header row
                "data": row_data
            })

    return results