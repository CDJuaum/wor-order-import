from datetime import datetime
from pathlib import Path


LOG_FOLDER = Path("logs")
LOG_FILE = LOG_FOLDER / "imports.log"


def log_import(service, workbook, sheet, row):
    """
    Records a successful Excel import.
    """

    LOG_FOLDER.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = (
        f"[{timestamp}]\n"
        f"Workbook: {workbook}\n"
        f"Sheet: {sheet}\n"
        f"Row: {row}\n"
        f"Client: {service.client}\n"
        f"Phone: {service.phone}\n"
        f"Service: {service.service}\n"
        f"Address: {service.address}\n"
        f"-------------------------\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(entry)