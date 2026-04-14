def execute(player, args, cmd=None):
    room = player.get("room")

    if not room:
        return "Non sei in una stanza valida."

    if not hasattr(room, "items") or not room.items:
        return "Non c'è nulla da lootare."

    # 🔍 cerca corpse
    target = None

    if args:
        name = " ".join(args).lower()

        for item in room.items:
            if name in item["name"].lower() and item.get("type") == "corpse":
                target = item
                break
    else:
        for item in room.items:
            if item.get("type") == "corpse":
                target = item
                break

    if not target:
        return "Nessun corpo trovato."

    loot = target.get("inventory", [])

    if not loot:
        return "Il corpo è vuoto."

    # 🎒 aggiungi inventario player
    if "inventory" not in player:
        player["inventory"] = []

    for item in loot:
        player["inventory"].append(item)

    # 🧹 svuota corpse
    target["inventory"] = []

    # 🗑️ rimuovi corpse se vuoto
    if not target["inventory"]:
        room.items.remove(target)

    return f"Hai saccheggiato {target['name']}."


description = "Saccheggia un corpo."
usage = "loot [nome]"