from core.world import get_room

def execute(player, conn, command, args):

    if not args:
        conn.send("Sblocca cosa?\n")
        return

    direction = args[0].lower()

    room = get_room(player["room"])
    exit = room.get("exits", {}).get(direction)

    if not exit:
        conn.send("Nessuna uscita.\n")
        return

    if not exit.get("locked"):
        conn.send("Non è bloccata.\n")
        return

    key = exit.get("key")

    if key not in player.get("inventory", []):
        conn.send("Non hai la chiave giusta.\n")
        return

    exit["locked"] = False

    conn.send("Sblocchi la porta.\n")