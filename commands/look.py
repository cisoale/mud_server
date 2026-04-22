from core.world import get_room

def render_room(*args):
    print("DEBUG render_room args:", args)

    player = args[0]  # forza compatibilità

    room = get_room(player["room"])

    if not room:
        return "Stanza inesistente.\n"

    return f"DEBUG ROOM: {room.name}\n"
# =========================
# UTILS
# =========================
def match_targets(name, objects):
    """
    Restituisce lista oggetti che matchano il nome
    """
    name = name.lower()
    matches = []

    for obj in objects:
        obj_name = obj.get("name", "").lower()
        if name in obj_name:
            matches.append(obj)

    return matches


def parse_target(args):
    """
    Gestisce:
    look goblin
    look goblin 2
    """
    if not args:
        return None, 1

    name = args[0]

    index = 1
    if len(args) > 1 and args[1].isdigit():
        index = int(args[1])

    return name, index


# =========================
# RENDER ROOM
# =========================
def render_room(player):

    room = get_room(player["room"])

    if not room:
        return "Stanza inesistente.\n"

    output = ""

    # titolo
    output += f"\n=== {room.name} ===\n"
    output += f"{room.description}\n\n"

    # =====================
    # USCITE
    # =====================
    output += "Uscite:\n"

    for direction, exit_data in room.exits.items():

        # supporta sia dict che int
        if isinstance(exit_data, dict):
            closed = exit_data.get("closed", False)
            secret = exit_data.get("secret", False)
        else:
            closed = False
            secret = False

        if secret:
            continue

        status = " (chiusa)" if closed else ""
        output += f" - {direction}{status}\n"

    # =====================
    # PLAYER
    # =====================
    others = [p for p in room.players if p != player]

    if others:
        output += "\nGiocatori presenti:\n"
        for p in others:
            output += f" - {p['name']}\n"

    # =====================
    # MOB
    # =====================
    if room.mobs:
        output += "\nCreature:\n"

        counts = {}

        for mob in room.mobs:
            name = mob["name"]
            counts[name] = counts.get(name, 0) + 1
            output += f" - {name} ({counts[name]})\n"

    # =====================
    # ITEMS / CORPI
    # =====================
    if room.items:
        output += "\nA terra:\n"

        counts = {}

        for item in room.items:

            # sicurezza: item può essere stringa
            if isinstance(item, str):
                name = item
            else:
                name = item.get("name", "oggetto")

            counts[name] = counts.get(name, 0) + 1
            output += f" - {name} ({counts[name]})\n"

    return output


# =========================
# LOOK COMMAND
# =========================
def execute(player, conn, args):

    room = get_room(player["room"])

    if not args:
        conn.send(render_room(player))
        return

    name, index = parse_target(args)

    # =====================
    # CERCA TRA OGGETTI
    # =====================
    targets = []

    # mobs
    targets += room.mobs

    # items
    for item in room.items:
        if isinstance(item, dict):
            targets.append(item)
        else:
            targets.append({"name": item})

    matches = match_targets(name, targets)

    if not matches or index > len(matches):
        conn.send("Non vedi nulla del genere.\n")
        return

    target = matches[index - 1]

    # =====================
    # DESCRIZIONE
    # =====================
    desc = target.get("description", "Niente di speciale.\n")

    conn.send(f"{target['name']}\n{desc}\n")

    # =====================
    # CORPSE LOOT PREVIEW
    # =====================
    if target.get("type") == "corpse":

        inventory = target.get("inventory", [])

        if inventory:
            conn.send("Contiene:\n")

            for item in inventory:
                if isinstance(item, dict):
                    conn.send(f" - {item.get('name', 'oggetto')}\n")
                else:
                    conn.send(f" - {item}\n")
        else:
            conn.send("È vuoto.\n")