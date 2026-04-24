from core.command_registry import get_commands


def cmd_help(player, args):

    commands = get_commands()

    grouped = {}

    # raggruppa per categoria
    for name, data in commands.items():
        cat = data["category"]

        if cat not in grouped:
            grouped[cat] = []

        grouped[cat].append((name, data["description"]))

    # output
    player["conn"].send("\n=== COMANDI DISPONIBILI ===\n")

    for cat, cmds in grouped.items():
        player["conn"].send(f"\n[{cat}]\n")

        for name, desc in cmds:
            player["conn"].send(f" - {name}: {desc}\n")

    player["conn"].send("\n")