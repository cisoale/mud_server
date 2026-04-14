def execute(player, conn, command, args):
    if not args:
        return "Lasciare cosa?"

    inv = player.get("inventory")
    room = player.get("room")

    target_name = " ".join(args).lower()

    for item in inv:
        if target_name in item["name"].lower():

            room.items.append(item)
            inv.remove(item)

            return f"Hai lasciato {item['name']}."

    return "Non hai quell'oggetto."