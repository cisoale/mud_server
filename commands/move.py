from core.world import get_room
from commands.look import execute as look


DIRECTIONS = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
    "u": "up",
    "d": "down",
    "north": "north",
    "south": "south",
    "east": "east",
    "west": "west",
    "up": "up",
    "down": "down",
}


def execute(player, conn, command, args):

    # =========================
    # DIREZIONE
    # =========================
    if command == "move":
        if not args:
            conn.send("Uso: move <direzione>\n")
            return
        raw_direction = args[0]
    else:
        raw_direction = command

    if not isinstance(raw_direction, str):
        conn.send("Errore direzione.\n")
        return

    direction = DIRECTIONS.get(raw_direction.lower())

    if not direction:
        conn.send("Direzione non valida.\n")
        return

    # =========================
    # ROOM ATTUALE
    # =========================
    room = get_room(player.get("room"))

    if not room:
        conn.send("Errore stanza.\n")
        return

    if direction not in room.exits:
        conn.send("Non puoi andare da quella parte.\n")
        return

    exit_data = room.exits[direction]

    # =========================
    # SUPPORTO NUOVO FORMATO EXIT
    # =========================
    if isinstance(exit_data, dict):

        # segreta
        if exit_data.get("secret"):
            conn.send("Non vedi nessuna uscita in quella direzione.\n")
            return

        # porta chiusa
        if exit_data.get("door") and exit_data.get("closed"):
            conn.send("La porta è chiusa.\n")
            return

        # porta bloccata
        if exit_data.get("locked"):
            conn.send("La porta è chiusa a chiave.\n")
            return

        next_room_vnum = exit_data.get("to")

    else:
        # compatibilità vecchio formato
        next_room_vnum = exit_data

    # =========================
    # VALIDAZIONE
    # =========================
    if not isinstance(next_room_vnum, int):
        conn.send("Errore destinazione.\n")
        return

    new_room = get_room(next_room_vnum)

    if not new_room:
        conn.send("La stanza non esiste.\n")
        return

    # =========================
    # RIMUOVI DA ROOM ATTUALE
    # =========================
    if hasattr(room, "players") and player in room.players:
        room.players.remove(player)

    # =========================
    # AGGIUNGI A NUOVA ROOM
    # =========================
    player["room"] = next_room_vnum

    if not hasattr(new_room, "players"):
        new_room.players = []

    new_room.players.append(player)

    conn.send(f"Vai verso {direction}.\n")

    # =========================
    # LOOK
    # =========================
    look(player, conn, "look", [])