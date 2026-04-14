def execute(player, conn, command, args):
    equipment = player.get("equipment", {})

    output = ["Equipaggiamento:"]

    for slot, item in equipment.items():
        if item:
            output.append(f"{slot}: {item['name']}")
        else:
            output.append(f"{slot}: (vuoto)")

    return "\n".join(output)