import pyperclip

def read_clipboard():
    """
    Reads the current content of the clipboard.
    """
    return pyperclip.paste()