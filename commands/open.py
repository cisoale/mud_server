def execute(player, conn, args):

    if not args:
        conn.send("Aprire cosa?\n")
        return

    direction = args[0].lower()

    from core.world import get_room
    room = get_room(player.get("room"))

    if direction not in room.exits:
        conn.send("Nessuna uscita.\n")
        return

    exit_data = room.exits[direction]

    if not isinstance(exit_data, dict) or not exit_data.get("door"):
        conn.send("Non c'è nessuna porta.\n")
        return

    if not exit_data.get("closed"):
        conn.send("È già aperta.\n")
        return

    if exit_data.get("locked"):
        conn.send("È chiusa a chiave.\n")
        return

    exit_data["closed"] = False

    conn.send("Apri la porta.\n")