import os
import importlib

commands = {}


# =========================
# CARICA COMANDI
# =========================
def load_commands():

    global commands
    commands.clear()

    commands_dir = "commands"

    for file in os.listdir(commands_dir):

        if not file.endswith(".py") or file.startswith("__"):
            continue

        name = file[:-3]

        try:
            module = importlib.import_module(f"commands.{name}")
            importlib.reload(module)

            if hasattr(module, "execute"):
                commands[name] = module.execute
                print(f"[CMD] Caricato: {name}")
            else:
                print(f"[ERRORE] {name} senza execute()")

        except Exception as e:
            print(f"[ERRORE COMANDO] {name}: {e}")

    # =========================
    # ALIAS MOVIMENTO
    # =========================
    if "move" in commands:

        commands["n"] = commands["move"]
        commands["s"] = commands["move"]
        commands["e"] = commands["move"]
        commands["w"] = commands["move"]
        commands["u"] = commands["move"]
        commands["d"] = commands["move"]

        commands["north"] = commands["move"]
        commands["south"] = commands["move"]
        commands["east"] = commands["move"]
        commands["west"] = commands["move"]
        commands["up"] = commands["move"]
        commands["down"] = commands["move"]


# =========================
# ESECUZIONE COMANDO
# =========================
def execute_command(player, conn, input_text):

    if not input_text:
        return

    parts = input_text.strip().split()

    command = parts[0].lower()
    args = parts[1:]

    print(f"[CMD] {player['name']}: {command} {args}")

    if command not in commands:
        conn.send("Comando sconosciuto.\n")
        return

    try:
        commands[command](player, conn, command, args)
    except Exception as e:
        print(f"[ERRORE COMANDO] {command}: {e}")
        conn.send("Errore durante l'esecuzione del comando.\n")


# =========================
# RELOAD LIVE
# =========================
def reload_commands():

    print("[CMD] Reload comandi...")
    load_commands()
    print("[CMD] Reload completato.")


# =========================
# LISTA COMANDI (per help)
# =========================
def get_all_commands():
    return list(commands.keys())