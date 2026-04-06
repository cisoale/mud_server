import importlib
import os

commands = {}

def load_commands():
    for file in os.listdir("commands"):
        if file.endswith(".py"):
            name = file[:-3]
            module = importlib.import_module(f"commands.{name}")

            commands[name] = module.execute

def handle_command(player, cmd_input):
    parts = cmd_input.split()
    
    if not parts:
        return "Comando vuoto."

    cmd = parts[0].lower()
    args = parts[1:]

    # abbreviazioni
    aliases = {
        "n": "north",
        "s": "south",
        "e": "east",
        "w": "west"
    }

    if cmd in aliases:
        cmd = aliases[cmd]

    if cmd in commands:
        return commands[cmd](player, args)

    return "Comando sconosciuto."