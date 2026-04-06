def execute(player, args, cmd=None):
    if not args:
        return "Equip cosa?"

    inv = player.get("inventory", [])
    equipment = player.get("equipment", {})

    try:
        index = int(args[0]) - 1
    except:
        return "Usa: equip <numero oggetto>"

    if index < 0 or index >= len(inv):
        return "Oggetto non valido."

    item = inv[index]
    slot = item.get("slot")

    if not slot:
        return "Non puoi equipaggiare questo oggetto."

    # se già equipaggiato qualcosa
    if equipment[slot]:
        inv.append(equipment[slot])

    equipment[slot] = item
    inv.pop(index)

    return f"Hai equipaggiato {item['name']} in {slot}."