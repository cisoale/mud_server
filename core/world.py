rooms = {}


class Room:
    def __init__(self, vnum, name, description, exits=None):
        self.vnum = vnum
        self.name = name
        self.description = description
        self.exits = exits or {}

        # 🔥 nuovi contenuti
        self.players = []
        self.mobs = []
        self.items = []


def load_world():
    global rooms

    rooms[1001] = Room(
        1001,
        "Villaggio umano",
        "Sei nel villaggio degli umani.",
        {"north": 1002}
    )

    rooms[1002] = Room(
        1002,
        "Strada polverosa",
        "Una strada che porta fuori dal villaggio.",
        {"south": 1001}
    )

    rooms[2001] = Room(
        2001,
        "Foresta elfica",
        "Una foresta luminosa e magica.",
        {"south": 2002}
    )

    rooms[2002] = Room(
        2002,
        "Radura elfica",
        "Una radura tranquilla.",
        {"north": 2001}
    )


def get_room(vnum):
    return rooms.get(vnum)