from core.command_handler import reload_commands

def execute(player, conn, command, args):

    if not player.get("builder"):
        conn.send("Non hai i permessi.\n")
        return

    reload_commands()

    conn.send("Comandi ricaricati.\n")