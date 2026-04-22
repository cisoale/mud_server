from core.world import get_room


def execute(player, conn, args):

    if not args:
        conn.send("Uso: unlock <direzione>\n")
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

    if not exit_data.get("locked"):
        conn.send("Non è chiusa a chiave.\n")
        return

    key_needed = exit_data.get("key")

    if key_needed:
        has_key = any(item.get("name") == key_needed for item in player["inventory"])
        if not has_key:
            conn.send("Non hai la chiave.\n")
            return

    exit_data["locked"] = False

    conn.send("Sblocchi la porta.\n")