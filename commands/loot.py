from core.world import get_room


# =========================
# UTILS
# =========================
def find_corpses(room, name):
    name = name.lower()
    matches = []

    for item in room.items:
        if isinstance(item, dict) and item.get("type") == "corpse":
            if name in item.get("name", "").lower():
                matches.append(item)

    return matches


def parse_args(args):
    """
    supporta:
    loot corpo
    loot corpo 2
    loot tutto corpo 2
    loot pugnale corpo 2
    """

    if not args:
        return None, None, 1

    if args[0] == "tutto":
        return "ALL", args[1] if len(args) > 1 else None, int(args[2]) if len(args) > 2 and args[2].isdigit() else 1

    if len(args) == 1:
        return None, args[0], 1

    if len(args) >= 2:
        item_name = args[0]
        corpse_name = args[1]

        index = 1
        if len(args) > 2 and args[2].isdigit():
            index = int(args[2])

        return item_name, corpse_name, index


# =========================
# LOOT COMMAND
# =========================
def execute(player, conn, args):

    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    item_name, corpse_name, index = parse_args(args)

    if not corpse_name:
        conn.send("Lootare cosa?\n")
        return

    corpses = find_corpses(room, corpse_name)

    if not corpses or index > len(corpses):
        conn.send("Non trovi quel corpo.\n")
        return

    corpse = corpses[index - 1]

    inventory = corpse.get("inventory", [])

    if not inventory:
        conn.send("Il corpo è vuoto.\n")
        return

    # =====================
    # LOOT TUTTO
    # =====================
    if item_name == "ALL":

        for item in inventory[:]:

            player.setdefault("inventory", []).append(item)
            inventory.remove(item)

            name = item["name"] if isinstance(item, dict) else item
            conn.send(f"Prendi {name}.\n")

        cleanup_corpse(room, corpse)
        return

    # =====================
    # LOOT SPECIFICO
    # =====================
    if item_name:

        for item in inventory:

            name = item["name"] if isinstance(item, dict) else item

            if item_name.lower() in name.lower():

                player.setdefault("inventory", []).append(item)
                inventory.remove(item)

                conn.send(f"Prendi {name}.\n")

                cleanup_corpse(room, corpse)
                return

        conn.send("Non trovi quell'oggetto.\n")
        return

    # =====================
    # LOOT DEFAULT (primo)
    # =====================
    item = inventory.pop(0)

    player.setdefault("inventory", []).append(item)

    name = item["name"] if isinstance(item, dict) else item
    conn.send(f"Prendi {name}.\n")

    cleanup_corpse(room, corpse)


# =========================
# CLEANUP CORPSE
# =========================
def cleanup_corpse(room, corpse):

    if not corpse.get("inventory"):
        if corpse in room.items:
            room.items.remove(corpse)