message = """
        24/07 14:00

        Install EV charger

        Rua da Liberdade 120

        João Silva - 912345678
"""

def parse_message(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:                    #ignores empty lines
            lines.append(line)
    return lines

for line in parse_message(message):
    print(line)