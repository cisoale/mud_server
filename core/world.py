# =========================
# STORAGE WORLD
# =========================
rooms = {}


# =========================
# ROOM CLASS
# =========================
class Room:

    def __init__(self, vnum, name, description=""):

        self.vnum = vnum
        self.name = name
        self.description = description

        self.exits = {}
        self.players = []
        self.mobs = []
        self.items = []

    def __repr__(self):
        return f"<Room {self.vnum}: {self.name}>"


# =========================
# ADD ROOM
# =========================
def add_room(vnum, name, description=""):

    room = Room(vnum, name, description)
    rooms[vnum] = room
    return room


# =========================
# GET ROOM
# =========================
def get_room(vnum):

    room = rooms.get(vnum)

    print(f"[DEBUG ROOM] {vnum} -> {type(room)}")

    return room

# =========================
# MOVE PLAYER
# =========================
def move_player(player, direction):

    room = get_room(player["room"])

    if not room:
        return None, "Stanza non trovata."

    if direction not in room.exits:
        return None, "Direzione non valida."

    new_room = get_room(room.exits[direction])

    if not new_room:
        return None, "Stanza non esistente."

    # rimuovi player dalla stanza attuale
    if player in room.players:
        room.players.remove(player)

    # aggiungi alla nuova
    new_room.players.append(player)
    player["room"] = new_room.vnum

    return new_room, None