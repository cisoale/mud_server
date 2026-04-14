import importlib
import os
import inspect

# 📦 dizionario comandi
commands = {}

# =========================
# 🔄 LOAD COMMANDS
# =========================
def load_commands():
    global commands
    commands = {}

    print("[COMMANDS] Caricamento...")

    for file in os.listdir("commands"):

        # salta file non validi
        if not file.endswith(".py") or file.startswith("__"):
            continue

        name = file[:-3]

        try:
            module = importlib.import_module(f"commands.{name}")

            if hasattr(module, "execute"):
                commands[name] = module.execute
                print(f"[OK] Comando caricato: {name}")
            else:
                print(f"[WARNING] {name}.py senza execute()")

        except Exception as e:
            print(f"[ERRORE] Caricamento {name}: {e}")

    print(f"[COMMANDS] Totale: {len(commands)}\n")


# =========================
# ⚡ EXECUTE COMMAND
# =========================
def execute_command(cmd, player, conn, args):

    cmd = cmd.lower()

    if cmd not in commands:
        conn.send("Comando sconosciuto.\n")
        return

    func = commands[cmd]

    try:
        func(player, conn, cmd, args)
    except Exception as e:
        print(f"[ERRORE COMANDO] {cmd}: {e}")
        conn.send(f"Errore nel comando {cmd}.\n")

# =========================
# 📜 LISTA COMANDI
# =========================
def get_all_commands():
    return list(commands.keys())

handle_command = execute_command