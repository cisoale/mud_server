from core.equipment import equip_item


def find_item(player, name):

    name = name.lower()

    matches = []

    for item in player.get("inventory", []):

        item_name = item.get("name", "").lower()

        if name in item_name:
            matches.append(item)

    if not matches:
        return None

    return matches[0]  # primo match


def execute(player, conn, args):

    if not args:
        conn.send("Cosa vuoi equipaggiare?\n")
        return

    name = " ".join(args)

    item = find_item(player, name)

    if not item:
        conn.send("Non possiedi questo oggetto.\n")
        return

    msg = equip_item(player, item)
    conn.send(msg + "\n")