import os
import importlib

commands = {}
aliases = {}

# =========================
# CARICAMENTO COMANDI
# =========================
def load_commands():
    global commands, aliases

    commands.clear()
    aliases.clear()

    base_path = os.path.join(os.path.dirname(__file__), "..", "commands")

    print("\n[CMD] Caricamento comandi...")

    for file in os.listdir(base_path):

        # ignora file non validi
        if not file.endswith(".py") or file.startswith("__"):
            continue

        name = file[:-3]

        try:
            module = importlib.import_module(f"commands.{name}")

            # 🔹 comando principale
            if hasattr(module, "execute"):
                commands[name] = module.execute
                print(f"[CMD] ✔ {name}")
            else:
                print(f"[CMD] ✖ {name} (manca execute())")
                continue

            # 🔹 alias opzionali
            if hasattr(module, "ALIASES"):
                for alias in module.ALIASES:
                    aliases[alias] = name

        except Exception as e:
            print(f"[ERRORE COMANDO] {name}: {e}")

    print(f"[CMD] Totale caricati: {len(commands)}")


# =========================
# ESECUZIONE COMANDO
# =========================
def execute_command(player, conn, input_text):

    if not input_text:
        return

    parts = input_text.strip().split()

    if not parts:
        return

    command = parts[0].lower()
    args = parts[1:]

    # =========================
    # ALIAS
    # =========================
    if command in aliases:
        command = aliases[command]

    # =========================
    # MOVIMENTO DIREZIONI
    # =========================
    directions = ["north", "south", "east", "west", "up", "down",
                  "n", "s", "e", "w", "u", "d"]

    if command in directions:
        move_cmd = commands.get("move")

        if not move_cmd:
            conn.send("Sistema movimento non disponibile.\n")
            return

        try:
            move_cmd(player, conn, [command])
        except Exception as e:
            print("[ERRORE MOVE]", e)
            conn.send("Errore movimento.\n")

        return

    # =========================
    # COMANDO NORMALE
    # =========================
    func = commands.get(command)

    if not func:
        conn.send("Comando sconosciuto.\n")
        return

    try:
        func(player, conn, args)

    except Exception as e:
        print(f"[CRASH COMANDO] {command}: {e}")
        conn.send("Errore comando.\n")


# =========================
# RELOAD COMANDI
# =========================
def reload_commands():
    print("[CMD] Reload comandi...")
    load_commands()