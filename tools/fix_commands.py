import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
COMMANDS_DIR = os.path.join(BASE_DIR, "commands")


def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # =========================
    # FIX conn.write -> conn.send
    # =========================
    content = re.sub(r'conn\.write\((.*?)\.encode\(\)\)', r'conn.send(\1)', content)

    # =========================
    # FIX firme execute
    # =========================
    content = re.sub(
        r'def execute\s*\(\s*player\s*,\s*conn\s*\)',
        'def execute(player, conn, command, args)',
        content
    )

    content = re.sub(
        r'def execute\s*\(\s*player\s*,\s*conn\s*,\s*command\s*\)',
        'def execute(player, conn, command, args)',
        content
    )

    # =========================
    # SE manca execute → aggiungi template
    # =========================
    if "def execute" not in content:
        content += """

def execute(player, conn, command, args):
    conn.send("Comando non ancora implementato.\\n")
"""

    # =========================
    # SALVA SOLO SE CAMBIATO
    # =========================
    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[FIXED] {path}")
    else:
        print(f"[OK] {path}")


def main():
    for file in os.listdir(COMMANDS_DIR):
        if file.endswith(".py") and not file.startswith("__"):
            fix_file(os.path.join(COMMANDS_DIR, file))


if __name__ == "__main__":
    main()