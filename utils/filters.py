import re

from parser.parser import PHONE_REGEX, INTERNATIONAL_PHONE_REGEX


def filter_clipboard_content(content: str) -> bool:
    """
    Checks if clipboard content resembles a work order.
    """

    if not content.strip():
        return False

    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    if len(lines) < 3:
        return False

    has_phone = (
        re.search(PHONE_REGEX, content)
        or re.search(INTERNATIONAL_PHONE_REGEX, content)
    )

    if not has_phone:
        return False

    return True
