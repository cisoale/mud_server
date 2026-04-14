from core.world import get_room

def execute(player, conn, command, args):

    if not args:
        conn.send("Apri cosa?\n")
        return

    direction = args[0].lower()

    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    exit = room.get("exits", {}).get(direction)

    if not exit:
        conn.send("Nessuna uscita in quella direzione.\n")
        return

    if not exit.get("door"):
        conn.send("Non c'è nessuna porta.\n")
        return

    if not exit.get("closed"):
        conn.send("È già aperta.\n")
        return

    if exit.get("locked"):
        conn.send("La porta è bloccata.\n")
        return

    exit["closed"] = False

    conn.send(f"Apri la porta verso {direction}.\n")