import win32gui
import ctypes
import pyperclip

from utils.filters import filter_clipboard_content

WM_CLIPBOARDUPDATE = 0x031D

def read_clipboard():
    """
    Reads the current content of the clipboard.
    """
    return pyperclip.paste()

class ClipboardListener:
    """
    Windows clipboard change listener.
    Calls callback whenever clipboard content changes.
    """

    instance = None

    def __init__(self, callback):
        self.callback = callback
        self.last_clipboard_content = ""
        ClipboardListener.instance = self

    def run(self):

        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = ClipboardListener._window_proc
        wc.lpszClassName = "ClipboardListener"

        class_atom = win32gui.RegisterClass(wc)

        hwnd = win32gui.CreateWindow(
            class_atom,
            "Clipboard Listener",
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            None,
        )

        ctypes.windll.user32.AddClipboardFormatListener(hwnd)

        print("Clipboard listener running...")

        win32gui.PumpMessages()

    @staticmethod
    def _window_proc(hwnd, msg, wparam, lparam):

        if msg == WM_CLIPBOARDUPDATE:

            text = read_clipboard().strip()

            if not text:
                return 0

            listener = ClipboardListener.instance

            if text == listener.last_clipboard_content:
                return 0

            listener.last_clipboard_content = text

            if not filter_clipboard_content(text):
                return 0
            
            listener.callback(text)

        return win32gui.DefWindowProc(
            hwnd,
            msg,
            wparam,
            lparam
        )