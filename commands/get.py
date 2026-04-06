def execute(player, args, cmd=None):
    if not args:
        return "Prendere cosa?"

    room = player.get("room")
    inv = player.get("inventory")

    target_name = " ".join(args).lower()

    for item in room.items:
        if target_name in item["name"].lower():

            inv.append(item)
            room.items.remove(item)

            return f"Hai preso {item['name']}."

    return "Non vedi nulla del genere."