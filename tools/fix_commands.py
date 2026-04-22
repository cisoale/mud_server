import os
import re

COMMANDS_DIR = "commands"


def fix_execute_signature(content):

    # trova execute
    pattern = r"def execute\s*\((.*?)\):"

    match = re.search(pattern, content)

    if not match:
        return content, False

    params = match.group(1)

    # già corretto
    if params.strip() == "player, conn, args":
        return content, False

    print(f"[FIX] Firma trovata: ({params}) -> (player, conn, args)")

    new_def = "def execute(player, conn, args):"

    content = re.sub(pattern, new_def, content, count=1)

    return content, True


def fix_missing_args_usage(content):

    # sostituisce input_text con args se presente
    content = re.sub(r"input_text", " ' '.join(args) ", content)

    return content


def fix_return_outside(content):

    # evita return fuori funzione (best effort)
    lines = content.split("\n")
    fixed = []

    inside_func = False

    for line in lines:

        if line.strip().startswith("def execute"):
            inside_func = True

        if line.strip().startswith("return") and not inside_func:
            print("[FIX] return fuori funzione rimosso")
            continue

        fixed.append(line)

    return "\n".join(fixed)


def process_file(path):

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    content, changed_sig = fix_execute_signature(content)
    content = fix_missing_args_usage(content)
    content = fix_return_outside(content)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[OK] Sistemato: {path}")
    else:
        print(f"[SKIP] {path}")


def main():

    if not os.path.exists(COMMANDS_DIR):
        print("[ERRORE] cartella commands non trovata")
        return

    print("\n=== FIX AUTOMATICO COMANDI ===\n")

    for file in os.listdir(COMMANDS_DIR):

        if not file.endswith(".py"):
            continue

        path = os.path.join(COMMANDS_DIR, file)

        process_file(path)

    print("\n=== COMPLETATO ===\n")


if __name__ == "__main__":
    main()