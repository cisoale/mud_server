from core.inventory import get_total_weight


def execute(player, conn, args):

    inv = player.get("inventory", [])

    if not inv:
        conn.send("Inventario vuoto.\n")
        return

    text = "\nInventario:\n"

    for item in inv:

        if isinstance(item, dict):
            name = item.get("name", "oggetto")
            weight = item.get("weight", 1)
        else:
            name = str(item)
            weight = 1

        text += f"- {name} (peso {weight})\n"

    total = get_total_weight(player)
    max_w = player.get("max_weight", 50)

    text += f"\nPeso: {total}/{max_w}\n"

    conn.send(text)