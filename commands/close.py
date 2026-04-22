from core.world import get_room


def execute(player, conn, args):

    if not args:
        conn.send("Uso: close <direzione>\n")
        return

    direction = args[0].lower()

    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    # ✅ FIX: usa attributo, non get()
    if direction not in room.exits:
        conn.send("Non c'è nulla lì.\n")
        return

    exit_data = room.exits[direction]

    if not isinstance(exit_data, dict) or not exit_data.get("door"):
        conn.send("Non c'è una porta.\n")
        return

    if exit_data.get("closed"):
        conn.send("È già chiusa.\n")
        return

    exit_data["closed"] = True

    conn.send("Chiudi la porta.\n")