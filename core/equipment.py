SLOTS = [
    "testa",
    "torso",
    "gambe",
    "piedi",
    "mani",
    "arma",
    "secondaria",
    "anello1",
    "anello2",
    "collo"
]


# =========================
# SLOT ANELLI
# =========================
def trova_slot_anello_libero(player):

    if "anello1" not in player["equipment"]:
        return "anello1"

    if "anello2" not in player["equipment"]:
        return "anello2"

    return None


# =========================
# EQUIP
# =========================
def equip_item(player, item):

    slot = item.get("slot")

    if not slot:
        return "Oggetto non equipaggiabile."

    slot = slot.lower()

    # gestione anelli
    if slot == "anello":
        slot = trova_slot_anello_libero(player)
        if not slot:
            return "Hai già due anelli equipaggiati."

    if slot not in SLOTS:
        return f"Slot non valido: {slot}"

    # oggetto già equipaggiato?
    if item in player["equipment"].values():
        return "Oggetto già equipaggiato."

    # rimuovi vecchio oggetto
    old_item = player["equipment"].get(slot)

    if old_item:
        player["inventory"].append(old_item)

    # equip
    player["equipment"][slot] = item

    # rimuovi da inventario
    if item in player["inventory"]:
        player["inventory"].remove(item)

    return f"Hai equipaggiato {item['name']} su {slot}."


# =========================
# UNEQUIP
# =========================
def unequip_item(player, slot):

    slot = slot.lower()

    if slot not in SLOTS:
        return "Slot non valido."

    item = player["equipment"].get(slot)

    if not item:
        return "Nessun oggetto in questo slot."

    player["inventory"].append(item)
    del player["equipment"][slot]

    return f"Hai rimosso {item['name']} da {slot}."