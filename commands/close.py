from core.world import get_room

def execute(player, conn, command, args):

    if not args:
        conn.send("Chiudi cosa?\n")
        return

    direction = args[0].lower()

    room = get_room(player["room"])
    exit = room.get("exits", {}).get(direction)

    if not exit or not exit.get("door"):
        conn.send("Nessuna porta.\n")
        return

    if exit.get("closed"):
        conn.send("È già chiusa.\n")
        return

    exit["closed"] = True

    conn.send(f"Chiudi la porta verso {direction}.\n")