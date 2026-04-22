import os
import importlib

commands = {}
aliases = {}

# =========================
# CARICAMENTO COMANDI
# =========================
def load_commands():

    global commands, aliases

    commands = {}
    aliases = {}

    base_path = os.path.join(os.path.dirname(__file__), "..", "commands")

    print("\n[CMD] Caricamento comandi...")

    for file in os.listdir(base_path):

        if not file.endswith(".py") or file.startswith("__"):
            continue

        name = file[:-3]

        try:
            module = importlib.import_module(f"commands.{name}")

            # ✅ REGISTRA COMANDO
            if hasattr(module, "execute"):
                commands[name] = module.execute
                print(f"[CMD] Caricato: {name}")
            else:
                print(f"[ERRORE] {name} non ha execute()")
                continue

            # ✅ ALIAS (opzionale)
            if hasattr(module, "ALIASES"):
                for alias in module.ALIASES:
                    aliases[alias] = name

        except Exception as e:
            print(f"[ERRORE COMANDO] {name}: {e}")

    print(f"[CMD] Totale: {len(commands)}")


# =========================
# ESECUZIONE COMANDO
# =========================
def execute_command(player, conn, input_text):

    if not input_text:
        return

    parts = input_text.strip().split()
    command = parts[0].lower()
    args = parts[1:]

    # 🔥 alias (n → north → move ecc)
    if command in aliases:
        command = aliases[command]

    # 🔥 shortcut direzioni
    directions = ["north", "south", "east", "west", "up", "down", "n", "s", "e", "w", "u", "d"]

    if command in directions:
        try:
            move_cmd = commands.get("move")
            if move_cmd:
                move_cmd(player, conn, [command])
            return
        except Exception as e:
            print("[ERRORE MOVE]", e)
            conn.send("Errore movimento.\n")
            return

    # 🔥 comando normale
    func = commands.get(command)

    if not func:
        conn.send("Comando sconosciuto.\n")
        return

    try:
        func(player, conn, args)
    except Exception as e:
        print(f"[CRASH COMANDO] {command}\n{e}")
        conn.send("Errore comando.\n")


# =========================
# RELOAD COMANDI
# =========================
def reload_commands():
    load_commands()