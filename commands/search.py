from core.world import get_room
import random

def execute(player, conn, command, args):

    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    found = False

    for direction, exit in room.get("exits", {}).items():

        if exit.get("secret"):

            # 🧠 puoi mettere probabilità
            if random.random() < 0.5:  # 50% chance
                exit["secret"] = False
                conn.send(f"Hai trovato un passaggio segreto verso {direction}!\n")
                return

    conn.send("Non trovi nulla di interessante.\n")