from core.world import get_room
from core.inventory import add_item


# =========================
# TROVA CORPO
# =========================
def find_corpse(room, name):

    name = name.lower()

    matches = []

    for item in room.items:

        if item.get("type") != "corpse":
            continue

        item_name = item.get("name", "").lower()

        if name in item_name:
            matches.append(item)

    if not matches:
        return None

    return matches[0]


# =========================
# COMANDO LOOT
# =========================
def execute(player, conn, args):

    room = get_room(player.get("room"))

    if not room:
        conn.send("Errore stanza.\n")
        return

    if not args:
        conn.send("Loot cosa?\n")
        return

    target_name = " ".join(args).lower()

    corpse = find_corpse(room, target_name)

    if not corpse:
        conn.send("Non trovi quel corpo.\n")
        return

    # =========================
    # LOOT OGGETTI
    # =========================
    loot_items = corpse.get("loot", [])

    if loot_items:
        conn.send("\nRecuperi:\n")

        for item in loot_items:

            add_item(player, item)

            name = item.get("name", "???")
            qty = item.get("quantity", 1)

            if qty > 1:
                conn.send(f"- {name} x{qty}\n")
            else:
                conn.send(f"- {name}\n")

    else:
        conn.send("Non trovi oggetti utili.\n")

    # =========================
    # GOLD
    # =========================
    gold = corpse.get("gold", 0)

    if gold > 0:
        player["gold"] = player.get("gold", 0) + gold
        conn.send(f"Hai trovato {gold} oro.\n")

    # =========================
    # RIMUOVI CORPO
    # =========================
    try:
        room.items.remove(corpse)
    except ValueError:
        pass

    conn.send("\nSaccheggio completato.\n")