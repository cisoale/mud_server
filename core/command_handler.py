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

    # 🔥 alias direzioni → tutte su move
    direction_aliases = {
        "n": "move",
        "north": "move",
        "s": "move",
        "south": "move",
        "e": "move",
        "east": "move",
        "w": "move",
        "west": "move",
        "u": "move",
        "up": "move",
        "d": "move",
        "down": "move"
    }

    if cmd in direction_aliases:
        command_name = direction_aliases[cmd]
    else:
        command_name = cmd

    if command_name in commands:
        return commands[command_name](player, args, cmd)
    
    if cmd == "exa":
        command_name = "examine"

    if cmd == "prendi":
        command_name = "get"
    
    if cmd == "lascia":
        command_name = "drop"

    return "Comando sconosciuto."