def execute(player, args, cmd=None):
    room = player.get("room")
    inv = player.get("inventory")

    if not args:
        return "Loot cosa?"

    target_name = " ".join(args).lower()

    # cerca corpse
    corpse = None
    for item in room.items:
        if item.get("type") == "corpse" and target_name in item["name"].lower():
            corpse = item
            break

    if not corpse:
        return "Nessun corpo trovato."

    corpse_inv = corpse.get("inventory", [])

    if not corpse_inv:
        return "Il corpo è vuoto."

    # trasferisci tutto
    for item in corpse_inv:
        inv.append(item)

    corpse["inventory"] = []

    return "Hai saccheggiato il corpo."