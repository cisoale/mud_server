def execute(player, conn, command, args):

    equipment = player.get("equipment", {})

    # =========================
    # SLOT STANDARD
    # =========================
    slots = [
        "weapon",
        "shield",
        "head",
        "torso",
        "legs",
        "feet",
        "hands",
        "ring",
        "amulet"
    ]

    text = "\n=== EQUIPAGGIAMENTO ===\n"

    for slot in slots:

        item = equipment.get(slot)

        if item:
            if isinstance(item, dict):
                name = item.get("name", "oggetto")
            else:
                name = str(item)
        else:
            name = "---"

        text += f"{slot.capitalize():<10}: {name}\n"

    text += "\n"

    conn.send(text)