def execute(player, args, cmd=None):
    if not args:
        return "Unequip cosa?"

    slot = args[0].lower()
    equipment = player.get("equipment", {})
    inv = player.get("inventory", [])

    if slot not in equipment:
        return "Slot non valido."

    item = equipment[slot]

    if not item:
        return "Niente da rimuovere."

    inv.append(item)
    equipment[slot] = None

    return f"Hai rimosso {item['name']}."