from pathlib import Path


WORKBOOK_FOLDER = Path("tests/workbooks")


def get_workbook_path(date: str) -> str:
    """
    Finds the workbook matching the service month.

    Example:
        24/07 -> 2026-07-Controle-Orcamentos.xlsx
    """

    print(WORKBOOK_FOLDER.resolve())
    
    day, month = date.split("/")

    pattern = f"*-{month}-Controle-Orcamentos.xlsx"

    matches = list(WORKBOOK_FOLDER.glob(pattern))

    if not matches:
        raise FileNotFoundError(
            f"No workbook found for month {month}"
        )

    if len(matches) > 1:
        raise RuntimeError(
            f"Multiple workbooks found for month {month}"
        )

    return str(matches[0])