from core.command_handler import get_all_commands

def execute(player, conn, command, args):

    cmds = get_all_commands()

    text = "\nComandi:\n"
    for c in sorted(cmds):
        text += f"- {c}\n"

    conn.send(text)