def execute(player, args, cmd=None):
    if not args:
        return "Examine cosa?"

    target_name = " ".join(args).lower()
    room = player.get("room")

    # 🔍 1. MOB
    for mob in room.mobs:
        if target_name in mob["name"].lower():
            return examine_mob(mob)

    # 🔍 2. OGGETTI A TERRA
    for item in room.items:
        if target_name in item["name"].lower():
            return examine_item(item)

    # 🔍 3. INVENTARIO
    for item in player.get("inventory", []):
        if target_name in item["name"].lower():
            return examine_item(item)

    # 🔍 4. EQUIP
    for item in player.get("equipment", {}).values():
        if item and target_name in item["name"].lower():
            return examine_item(item)

    return "Non vedi nulla del genere."