rooms = {}

class Room:
    def __init__(self, vnum, name, description, exits=None):
        self.vnum = vnum
        self.name = name
        self.description = description
        self.exits = exits or {}

        self.players = []
        self.mobs = []
        self.items = []


def load_world():
    global rooms

    from core.mob_factory import create_mob

    # 🏠 UMANI
    rooms[1001] = Room(
        1001,
        "Villaggio umano",
        "Sei nel villaggio degli umani.",
        {"north": 1002}
    )

    rooms[1002] = Room(
        1002,
        "Strada polverosa",
        "Una strada polverosa.",
        {"south": 1001}
    )

    # 🌲 ELFI
    rooms[2001] = Room(
        2001,
        "Foresta elfica",
        "Una foresta luminosa.",
        {"south": 2002}
    )

    rooms[2002] = Room(
        2002,
        "Radura elfica",
        "Una radura tranquilla.",
        {"north": 2001}
    )

    # 👹 MOB
    goblin = create_mob(
        "goblin",
        "Un piccolo goblin verde ti osserva.",
        10,
        inventory=[
            {"name": "Daga", "slot": "weapon"},
            {"name": "Monete"}
        ]
    )

    rooms[1001].mobs.append(goblin)


def get_room(vnum):
    return rooms.get(vnum)