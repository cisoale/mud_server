def get_opposite_direction(direction):

    opposites = {
        "north": "south",
        "south": "north",
        "east": "west",
        "west": "east",
        "up": "down",
        "down": "up"
    }

    return opposites.get(direction)

def broadcast_room(room, message, exclude=None):

    if not hasattr(room, "players"):
        return

    for p in room.players:

        if exclude and p == exclude:
            continue

        conn = p.get("conn")

        if conn:
            try:
                conn.send(message)
            except:
                pass