name = "help"
category = "system"
description = "Mostra tutti i comandi disponibili"
usage = "help [comando]"


def execute(player, conn, args):

    from core.command_handler import commands

    # =========================
    # HELP SPECIFICO
    # =========================
    if args:
        cmd = args[0]

        if cmd in commands:
            c = commands[cmd]

            msg = f"\n{c['name'].upper()}\n"
            msg += f"Descrizione: {c['description']}\n"
            msg += f"Uso: {c['usage']}\n"

            conn.send(msg)
        else:
            conn.send("Comando non trovato.\n")

        return

    # =========================
    # LISTA PER CATEGORIA
    # =========================
    categories = {}

    for cmd_name, data in commands.items():

        cat = data["category"]

        if cat not in categories:
            categories[cat] = []

        categories[cat].append(cmd_name)

    msg = "\n=== COMANDI ===\n"

    for cat in sorted(categories):

        msg += f"\n[{cat.upper()}]\n"

        for cmd in sorted(categories[cat]):
            msg += f" - {cmd}\n"

    msg += "\nDigita 'help <comando>' per dettagli.\n"

    conn.send(msg)