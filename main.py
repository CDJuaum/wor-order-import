from parser.parser import parse_message
from excel.writer import write_service
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


def main():

    print("WhatsApp Excel Importer")
    print("======================")
    print("Paste the WhatsApp message.")
    print("Finish by pressing ENTER twice.\n")

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    message = "\n".join(lines)

    if not message.strip():
        print("No message entered.")
        return

    service = parse_message(message)

    print_service(service)

    confirm = input("\nImport to Excel? (y/n): ").lower()

    workbook_path = get_workbook_path(service.date)

    if confirm == "y":
        workbook_path, sheet_name, row = write_service(
            service,
            workbook_path
        )

        print(f"Imported successfully to {workbook_path}")
        print(f"Sheet: {sheet_name}, Row: {row}")

        log_import(service, workbook_path, sheet_name, row)

    else:
        print("Cancelled.")


if __name__ == "__main__":
    main()