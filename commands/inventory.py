def execute(player, conn, args):

    inventory = player.get("inventory", [])

    if not inventory:
        conn.send("Il tuo inventario è vuoto.\n")
        return

    conn.send("\nInventario:\n")

    counts = {}

    for item in inventory:

        # sicurezza: item deve essere dict
        if not isinstance(item, dict):
            print(f"[BUG INVENTORY] Item non valido: {item}")
            continue

        # nome visivo
        name = item.get("display_name") or item.get("name", "oggetto sconosciuto")

        if not isinstance(name, str):
            name = "oggetto corrotto"

        # quantità
        qty = item.get("quantity", 1)

        if not isinstance(qty, int):
            qty = 1

        counts[name] = counts.get(name, 0) + qty

    # stampa finale
    for name, qty in counts.items():
        if qty > 1:
            conn.send(f" - {name} x{qty}\n")
        else:
            conn.send(f" - {name}\n")

    conn.send("\n")