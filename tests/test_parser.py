import json
from datetime import datetime
from dataclasses import asdict

from parser.parser import parse_message

REFERENCE_DATE = datetime(2026, 7, 23)

with open("tests/samples.json", encoding="utf-8") as f:
    samples = json.load(f)

passed = 0
failed = 0

for sample in samples:

    service = parse_message(
        sample["message"],
        reference_date=REFERENCE_DATE
    )

    actual = asdict(service)
    expected = sample["expected"]

    errors = []

    for key, expected_value in expected.items():

        actual_value = actual[key]

        if actual_value != expected_value:
            errors.append(
                f"{key}: expected '{expected_value}', got '{actual_value}'"
            )

    if errors:
        failed += 1

        print(f"\n✗ {sample['name']}")

        for error in errors:
            print(f"    {error}")

    else:
        passed += 1
        print(f"✓ {sample['name']}")

print("\n-------------------------")
print(f"Passed: {passed}")
print(f"Failed: {failed}")