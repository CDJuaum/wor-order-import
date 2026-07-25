from openpyxl import load_workbook
from parser.parser import format_phone_for_excel


def get_sheet_name(date: str) -> str:
    """
    Converts DD/MM into the workbook sheet name.

    Example:
        24/07 -> "24"
    """
    day = date.split("/")[0]

    return str(int(day))  # Remove leading zeros
    

def find_next_row(sheet):
    """
    Finds the first empty row.
    Data starts at row 2.
    """
    row = 2

    while sheet[f"A{row}"].value is not None:
        row += 1

    return row


def write_service(service, workbook_path: str):
    """
    Writes a Service object into the correct day sheet.
    """

    workbook = load_workbook(workbook_path)

    sheet_name = get_sheet_name(service.date)

    sheet = workbook[sheet_name]

    row = find_next_row(sheet)

    sheet[f"A{row}"] = service.date
    sheet[f"B{row}"] = service.time
    sheet[f"C{row}"] = service.tag
    sheet[f"D{row}"] = service.service
    sheet[f"E{row}"] = service.address
    sheet[f"F{row}"] = format_phone_for_excel(service.phone)
    sheet[f"G{row}"] = service.client

    workbook.save(workbook_path)

    return sheet_name, row