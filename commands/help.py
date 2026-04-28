# =========================
# HELP COMMAND
# =========================

def execute(player, conn, args):

    from core.command_handler import commands, aliases

    # =========================
    # HELP SPECIFICO
    # =========================
    if args:
        cmd = args[0].lower()

        if cmd in aliases:
            cmd = aliases[cmd]

        func = commands.get(cmd)

        if not func:
            conn.send("Comando non trovato.\n")
            return

        # prova a leggere docstring
        desc = func.__doc__ or "Nessuna descrizione disponibile."

        conn.send(f"\n=== HELP: {cmd} ===\n")
        conn.send(desc.strip() + "\n")

        # alias collegati
        related_aliases = [a for a, c in aliases.items() if c == cmd]

        if related_aliases:
            conn.send(f"Alias: {', '.join(related_aliases)}\n")

        return

    # =========================
    # LISTA COMANDI
    # =========================
    conn.send("\n=== COMANDI DISPONIBILI ===\n")

    sorted_cmds = sorted(commands.keys())

    for cmd in sorted_cmds:

        func = commands[cmd]

        desc = func.__doc__.split("\n")[0] if func.__doc__ else ""

        conn.send(f"- {cmd:10} {desc}\n")

    conn.send("\nUsa: help <comando> per dettagli\n")