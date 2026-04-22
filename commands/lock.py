from core.world import get_room


def execute(player, conn, args):

    if not args:
        conn.send("Uso: lock <direzione>\n")
        return

    direction = args[0].lower()
    room = get_room(player["room"])

    if direction not in room.exits:
        conn.send("Non c'è nulla lì.\n")
        return

    exit_data = room.exits[direction]

    if not isinstance(exit_data, dict) or not exit_data.get("door"):
        conn.send("Non c'è una porta.\n")
        return

    if exit_data.get("locked"):
        conn.send("È già chiusa a chiave.\n")
        return

    key_needed = exit_data.get("key")

    if key_needed:
        has_key = any(item.get("name") == key_needed for item in player["inventory"])
        if not has_key:
            conn.send("Non hai la chiave.\n")
            return

    exit_data["locked"] = True
    exit_data["closed"] = True

    conn.send("Chiudi e blocchi la porta.\n")