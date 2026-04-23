def execute(player, conn, args):

    inv = player.get("inventory", [])

    if not inv:
        conn.send("Inventario vuoto.\n")
        return

    conn.send("\n--- Inventario ---\n")

    for item in inv:

        name = item.get("name", "???")
        qty = item.get("quantity", 1)

        if qty > 1:
            conn.send(f"{name} x{qty}\n")
        else:
            conn.send(f"{name}\n")