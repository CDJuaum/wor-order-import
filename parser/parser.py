import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timedelta



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

WEEKDAYS = {
    "segunda": 0,
    "terca": 1,
    "terça": 1,
    "quarta": 2,
    "quinta": 3,
    "sexta": 4,
    "sabado": 5,
    "sábado": 5,
    "domingo": 6,
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
    """
    text = normalize(text)

    if re.search(r"\d{1,2}[/-]\d{1,2}", text):
        return True

    if re.search(r"\d{1,2}(?:h|:\d{2})", text):
        return True

    if "amanha" in text:
        return True

    if any(day in text for day in WEEKDAYS):
        return True

    return False


def extract_datetime(
    text: str,
    reference_date: datetime | None = None
) -> tuple[str | None, str | None]:
    
    text = normalize(text)

    if reference_date is None:
        reference_date = datetime.today()

    today = reference_date

    date = today.strftime("%d/%m")
    time = None

    # -------------------------
    # Explicit date
    # -------------------------

    date_match = re.search(r"(\d{1,2})[/-](\d{1,2})", text)

    if date_match:
        day = int(date_match.group(1))
        month = int(date_match.group(2))

        date = f"{day:02d}/{month:02d}"

    # -------------------------
    # Tomorrow
    # -------------------------

    elif "amanha" in text:
        tomorrow = today + timedelta(days=1)
        date = tomorrow.strftime("%d/%m")

    # -------------------------
    # Weekday
    # -------------------------

    else:
        for weekday_name, weekday_number in WEEKDAYS.items():

            if weekday_name in text:

                days_ahead = (weekday_number - today.weekday()) % 7

                if days_ahead == 0:
                    days_ahead = 7

                target = today + timedelta(days=days_ahead)

                date = target.strftime("%d/%m")
                break

    # -------------------------
    # Time
    # -------------------------

    time_match = re.search(r"(\d{1,2})(?:h|:)(\d{2})?", text)

    if time_match:

        hour = int(time_match.group(1))

        minutes = time_match.group(2)

        if minutes is None:
            minutes = "00"

        time = f"{hour:02d}:{minutes}"

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

def parse_message(
    message: str,
    reference_date: datetime | None = None
) -> Service:

    lines = clean_lines(message)

    if reference_date is None:
        reference_date = datetime.today()

    result = Service(
        date=reference_date.strftime("%d/%m")
    )

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
        quarta 10h

        Install EV Charger

        Rua da Liberdade 120
        Lisboa 1150-214

        João Silva - 912345678 211234567
"""

    service = parse_message(sample)

    print(service)