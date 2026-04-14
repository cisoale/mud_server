from core.world import get_room
from commands.look import render_room

DIRECTIONS = ["north", "south", "east", "west", "up", "down"]

def execute(player, conn, command, args):

    direction = command.lower()

    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    exit = room.exits.get(direction)

    if not exit:
        conn.send("Non puoi andare lì.\n")
        return

    if exit.get("door") and exit.get("closed"):
        conn.send("La porta è chiusa.\n")
        return

    player["room"] = exit["to"]

    conn.send(f"Vai verso {direction}.\n")
    conn.send(render_room(player))