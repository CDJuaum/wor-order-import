from utils.processor import process_message
from utils.clipboard_monitor import ClipboardListener


def main():

    print("WhatsApp Excel Importer")
    print("======================")
    print("Waiting for clipboard service messages...\n")

    listener = ClipboardListener(process_message)

    listener.run()


if __name__ == "__main__":
    main()