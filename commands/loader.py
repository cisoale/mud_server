import importlib
import os

commands = {}

def load_commands():
    for file in os.listdir("commands"):
        if file.endswith(".py"):
            name = file[:-3]
            module = importlib.import_module(f"commands.{name}")
            commands[name] = module.execute