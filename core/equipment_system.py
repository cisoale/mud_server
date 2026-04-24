from core.inventory import remove_item, add_item, find_item
from core.loot_system import get_item_data


# =========================
# INIT EQUIPMENT
# =========================
def init_equipment(player):

    player.setdefault("equipment", {
        "weapon": None,
        "head": None,
        "chest": None,
        "legs": None,
        "feet": None,
        "hands": None,
        "shield": None,
        "ring": None,
        "amulet": None
    })


# =========================
# EQUIP ITEM
# =========================
def equip_item(player, item_name):

    init_equipment(player)

    item = find_item(player, item_name)

    if not item:
        return False, "Non possiedi questo oggetto."

    item_data = get_item_data(item["name"])

    slot = item_data.get("slot")

    if not slot:
        return False, "Questo oggetto non è equipaggiabile."

    equipment = player["equipment"]

    # se già equip → swap
    if equipment.get(slot):
        old_item = equipment[slot]

        add_item(player, old_item["name"], old_item.get("quantity", 1))

    # rimuovi da inventario
    remove_item(player, item["name"], 1)

    # equip
    equipment[slot] = {
        "name": item["name"]
    }

    return True, f"Hai equipaggiato {item['name']}."


# =========================
# UNEQUIP
# =========================
def unequip_item(player, slot):

    init_equipment(player)

    equipment = player["equipment"]

    if slot not in equipment:
        return False, "Slot non valido."

    item = equipment.get(slot)

    if not item:
        return False, "Nessun oggetto equipaggiato."

    # torna in inventario
    add_item(player, item["name"], 1)

    equipment[slot] = None

    return True, f"Hai rimosso {item['name']}."


# =========================
# BONUS CALCOLO
# =========================
def get_equipment_bonus(player):

    total = {
        "damage": 0,
        "defense": 0
    }

    for slot, item in player.get("equipment", {}).items():

        if not item:
            continue

        data = get_item_data(item["name"])

        total["damage"] += data.get("damage", 0)
        total["defense"] += data.get("defense", 0)

    return total


# =========================
# MOSTRA EQUIP
# =========================
def format_equipment(player):

    init_equipment(player)

    equipment = player["equipment"]

    lines = ["Equipaggiamento:"]

    for slot, item in equipment.items():
        if item:
            lines.append(f"{slot}: {item['name']}")
        else:
            lines.append(f"{slot}: (vuoto)")

    return "\n".join(lines) + "\n"