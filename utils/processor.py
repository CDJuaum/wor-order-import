from parser.parser import parse_message
from excel.writer import write_service
from excel.checks import is_duplicate
from excel.workbook import get_workbook_path
from utils.logger import log_import


def print_service(service):
    print("\nDetected service:")
    print("-----------------")
    print(f"Date:    {service.date}")
    print(f"Hour:    {service.time}")
    print(f"Tag:     {service.tag}")
    print(f"Service: {service.service}")
    print(f"Address: {service.address}")
    print(f"Client:  {service.client}")
    print(f"Phone:   {service.phone}")
    print("-----------------")


def process_message(message):

    service = parse_message(message)

    errors, warnings = service.validation_errors()

    if errors:
        print("\nInvalid service data:")
        for error in errors:
            print(f"- {error}")
        return

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    print_service(service)

    confirm = input("\nImport to Excel? (y/n): ").lower()

    if confirm != "y":
        print("Cancelled.")
        return

    try:
        workbook_path = get_workbook_path(service.date)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    except RuntimeError as e:
        print(f"Error: {e}")
        return

    try:
        if is_duplicate(workbook_path, service):
            print("\nPossible duplicate detected.")

            duplicate_confirm = input(
                "Import anyway? (y/n): "
            ).lower()

            if duplicate_confirm != "y":
                print("Cancelled.")
                return

        workbook_path, sheet_name, row = write_service(
            service,
            workbook_path
        )

    except PermissionError:
        print(
            f"Error: Could not access {workbook_path}. "
            "Make sure the file is closed and try again."
        )
        return

    except KeyError as e:
        print(f"Error: Sheet not found: {e}")
        return

    print(f"Imported successfully to {workbook_path}")
    print(f"Sheet: {sheet_name}, Row: {row}")

    log_import(
        service,
        workbook_path,
        sheet_name,
        row
    )