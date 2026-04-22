from core.command_handler import reload_commands


def execute(player, conn, args):
    reload_commands()
    conn.send("Comandi ricaricati.\n")