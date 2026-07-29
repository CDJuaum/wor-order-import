import re

from parser.parser import PHONE_REGEX, INTERNATIONAL_PHONE_REGEX


def filter_clipboard_content(content: str) -> bool:
    """
    Checks if clipboard content resembles a work order.
    """

    if not content.strip():
        return False, "Clipboard content is empty."

    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    if len(lines) < 3:
        return False, "Clipboard content does not have enough lines to be a work order."

    has_phone = (
        re.search(PHONE_REGEX, content)
        or re.search(INTERNATIONAL_PHONE_REGEX, content)
    )

    if not has_phone:
        return False, "Clipboard content does not contain a valid phone number."

    return True
