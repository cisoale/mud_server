from core.world import get_room
from commands.look import render_room


# =========================
# ALIAS DIREZIONI
# =========================
DIRECTIONS = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
    "u": "up",
    "d": "down"
}


# =========================
# BROADCAST ROOM
# =========================
def broadcast(room, message, exclude=None):
    for p in room.players:
        if exclude and p == exclude:
            continue

        conn = p.get("conn")
        if conn:
            conn.send(message)


# =========================
# DIREZIONE OPPOSTA
# =========================
OPPOSITES = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
    "up": "down",
    "down": "up"
}


# =========================
# MOVE COMMAND
# =========================
def execute(player, conn, args):

    # =========================
    # DIREZIONE INPUT
    # =========================
    if not args:
        conn.send("Dove vuoi andare?\n")
        return

    direction = args[0].lower()
    direction = DIRECTIONS.get(direction, direction)

    # =========================
    # ROOM ATTUALE
    # =========================
    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    if direction not in room.exits:
        conn.send("Direzione non valida.\n")
        return

    exit_data = room.exits[direction]

    # =========================
    # SUPPORTO EXIT (dict/int)
    # =========================
    if isinstance(exit_data, dict):
        to_room = exit_data.get("to")
        closed = exit_data.get("closed", False)
        locked = exit_data.get("locked", False)
    else:
        to_room = exit_data
        closed = False
        locked = False

    # =========================
    # CONTROLLI PORTE
    # =========================
    if locked:
        conn.send("La porta è chiusa a chiave.\n")
        return

    if closed:
        conn.send("La porta è chiusa.\n")
        return

    # =========================
    # DESTINAZIONE
    # =========================
    new_room = get_room(to_room)

    if not new_room:
        conn.send("La stanza di destinazione non esiste.\n")
        return

    # =========================
    # USCITA PLAYER
    # =========================
    broadcast(
        room,
        f"{player['name']} esce verso {direction}.\n",
        exclude=player
    )

    # rimuovi da vecchia room
    if player in room.players:
        room.players.remove(player)

    # =========================
    # ENTRATA PLAYER
    # =========================
    new_room.players.append(player)
    player["room"] = to_room

    opposite = OPPOSITES.get(direction, "qualcosa")

    broadcast(
        new_room,
        f"{player['name']} entra da {opposite}.\n",
        exclude=player
    )

    # =========================
    # FEEDBACK PLAYER
    # =========================
    conn.send(f"Vai verso {direction}.\n")

    # =========================
    # MOSTRA ROOM
    # =========================
    conn.send(render_room(player))