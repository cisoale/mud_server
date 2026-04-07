def execute(player, args, cmd=None):
    if not args:
        return "Examine cosa?"

    target_name = " ".join(args).lower()
    room = player.get("room")

    # 🔍 MOB
    for mob in room.mobs:
        if target_name in mob["name"].lower():
            return examine_mob(mob)

    # 🔍 OGGETTI A TERRA
    for item in room.items:
        if target_name in item["name"].lower():
            return examine_item(item)

    # 🔍 INVENTARIO
    for item in player.get("inventory", []):
        if target_name in item["name"].lower():
            return examine_item(item)

    # 🔍 EQUIP
    for item in player.get("equipment", {}).values():
        if item and target_name in item["name"].lower():
            return examine_item(item)

    return "Non vedi nulla del genere."


# 👹 MOB
def examine_mob(mob):
    output = []

    output.append(mob["name"])
    output.append(f"HP: {mob.get('hp', '?')}")

    if mob.get("description"):
        output.append(mob["description"])

    if mob.get("inventory"):
        output.append("Sembra avere qualcosa con sé.")

    return "\n".join(output)


# 🎒 ITEM
def examine_item(item):
    output = []

    output.append(item["name"])

    if item.get("description"):
        output.append(item["description"])

    # ⚔️ danno
    if item.get("damage"):
        output.append(f"Danno: {item['damage']}")

    # 🛡️ armatura
    if item.get("armor"):
        output.append(f"Armatura: {item['armor']}")

    # ⚰️ corpse
    if item.get("type") == "corpse":
        inv = item.get("inventory", [])

        if inv:
            output.append("Contiene:")
            for i in inv:
                output.append(f" - {i['name']}")
        else:
            output.append("È vuoto.")

    return "\n".join(output)