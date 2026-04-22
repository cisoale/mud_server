from core.world import get_room


def execute(player, conn, args):

    room = get_room(player["room"])

    if not room:
        conn.send("Non sei in una stanza valida.\n")
        return

    found = False

    # 🔍 ciclo corretto
    for direction, exit_data in room.exits.items():

        if exit_data.get("secret"):

            exit_data["secret"] = False
            conn.send(f"Hai trovato un passaggio segreto verso {direction}!\n")
            found = True

    if not found:
        conn.send("Non trovi nulla di interessante.\n")