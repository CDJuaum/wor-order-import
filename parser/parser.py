import re
import unicodedata
from dataclasses import dataclass



# ==========================
# Data model
# ==========================

@dataclass
class Service:
    tag: str = "P"

    date: str | None = None
    time: str | None = None
    service: str | None = None
    address: str | None = None
    client: str | None = None
    phone: str | None = None

# ==========================
# Constants
# ==========================    

PHONE_REGEX = (
    r"(?:\+351[\s-]?)?[29]\d{8}"
    r"(?:\s*(?:/\s*)?(?:\+351[\s-]?)?[29]\d{8})?"
)

# ==========================
# Helper functions
# ==========================

def normalize(text: str) -> str:
    """
    Lowercase and remove accents.
    """
    text = text.lower()

    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )

    return text.strip()

REPAIR_TAGS = {
    normalize("rep casa"),
    normalize("reparacoes casa"),
    normalize("reparações casa"),
    normalize("reparacoes em casa"),
    normalize("reparações em casa"),
    normalize("rep em casa"),
}

def clean_lines(message: str) -> list[str]:
    """
    Removes empty lines and leading/trailing whitespace.
    """
    return [line.strip() for line in message.splitlines() if line.strip()]


def looks_like_phone(text: str) -> bool:
    """
    Detects Portuguese phone numbers.
    """
    phone_regex = r"\b(?:\+351\s?)?[29]\d{8}\b"
    return re.search(phone_regex, text) is not None


def looks_like_datetime(text: str) -> bool:
    """
    Detects common date/time formats.

    Examples:
        24/07
        24/07 14:30
        24-07
        14:30
    """
    patterns = [
        r"\d{1,2}[/-]\d{1,2}",
        r"\d{1,2}:\d{2}",
    ]

    return any(re.search(pattern, text) for pattern in patterns)


def extract_datetime(text: str) -> tuple[str | None, str | None]:
    date = None
    time = None

    date_match = re.search(r"\d{1,2}[/-]\d{1,2}", text)
    time_match = re.search(r"\d{1,2}:\d{2}", text)

    if date_match:
        date = date_match.group()

    if time_match:
        time = time_match.group()

    return date, time


def extract_client_phone(text: str) -> tuple[str | None, str | None]:
    """
    Extracts:
        João Silva - 912345678

    Returns:
        ("João Silva", "912345678")
    """

    phone_regex = (
        r"(?:\+351[\s-]?)?[29]\d{8}"
        r"(?:\s*(?:/\s*)?(?:\+351[\s-]?)?[29]\d{8})?"
    )

    match = re.search(phone_regex, text)

    if not match:
        return text.strip(), None

    phone = match.group().strip()

    # Standardize formatting
    numbers = re.findall(r"(?:\+351[\s-]?)?[29]\d{8}", phone)
    phone = " / ".join(numbers)

    client = text.replace(match.group(), "")
    client = client.replace("-", "").strip()

    return client, phone

def extract_tag(lines: list[str]) -> tuple[str, list[str]]:
    """
    Returns the service tag and removes the tag line from the message.

    Default tag: P
    Repair-at-home services: C
    """

    remaining = []

    tag = "P"

    for line in lines:
        if normalize(line) in REPAIR_TAGS:
            tag = "C"
        else:
            remaining.append(line)

    return tag, remaining

# ==========================
# Main parser
# ==========================

def parse_message(message: str) -> Service:

    lines = clean_lines(message)

    result = Service()

    # Detect tag
    result.tag, lines = extract_tag(lines)

    # Detect date/time
    if lines and looks_like_datetime(lines[0]):
        result.date, result.time = extract_datetime(lines.pop(0))

    # Client
    if lines:
        result.client, result.phone = extract_client_phone(lines.pop())

    # Service
    if lines:
        result.service = lines.pop(0)

    # Address
    if lines:
        result.address = " ".join(lines)

    return result

# ==========================
# Testing
# ==========================

if __name__ == "__main__":

    sample = """
        24/07 14:30

        Install EV Charger

        Rua da Liberdade 120
        Lisboa

        João Silva - 912345678 211234567
        
"""

    service = parse_message(sample)

    print(service)