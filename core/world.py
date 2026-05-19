rooms = {}


class Room:
    def __init__(self, vnum, name, description, region="starting_region"):
        self.vnum = vnum
        self.name = name
        self.description = description

        # Living World
        self.region_id = region

        self.players = []
        self.mobs = []
        self.items = []
        self.exits = {}

    def __repr__(self):
        return f"<Room {self.vnum}: {self.name}>"

def add_room(vnum, name, description="", region="starting_region"):
    room = Room(vnum, name, description, region)
    rooms[vnum] = room
    return room


def get_room(vnum):
    if isinstance(vnum, Room):
        return vnum
    return rooms.get(vnum)


def move_player(player, direction):

    room = get_room(player["room"])

    if not room:
        return None, "Stanza non trovata."

    if direction not in room.exits:
        return None, "Direzione non valida."

    exit_data = room.exits[direction]

    if isinstance(exit_data, dict):
        target = exit_data.get("to")
    else:
        target = exit_data

    new_room = get_room(target)
    print(f"[DEBUG] Entrato in regione: {new_room.region_id}")
    if not new_room:
        return None, "Stanza non esistente."

    if player in room.players:
        room.players.remove(player)

    new_room.players.append(player)
    player["room"] = new_room.vnum

    return new_room, None

def broadcast_room(room, message, exclude=None):

    for player in room.players:
        conn = player.get("conn")

        if not conn:
            continue

        if exclude and player == exclude:
            continue

        try:
            conn.send(message)
        except:
            pass