from core.world import get_room
from core.combat_system import start_combat


def execute(player, conn, args):

    if not args:
        conn.send("Attacca cosa?\n")
        return

    room = get_room(player["room"])
    if not room:
        conn.send("Errore stanza.\n")
        return

    target_name = " ".join(args).lower()

    for mob in room.mobs:
        if mob["name"].lower() == target_name:
            start_combat(player, mob, conn)
            return

    conn.send("Nessun bersaglio trovato.\n")