from core.world import get_room


def execute(player, conn, args):

    fixed_inv = 0
    removed_inv = 0

    # =========================
    # FIX INVENTORY
    # =========================
    new_inventory = []

    for item in player.get("inventory", []):

        # caso corretto
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            new_inventory.append(item)
            continue

        # caso stringa → converti
        if isinstance(item, str):
            new_item = {
                "name": item.replace(" ", "_"),
                "display_name": item.title(),
                "quantity": 1
            }
            new_inventory.append(new_item)
            fixed_inv += 1
            continue

        # caso corrotto → elimina
        removed_inv += 1

    player["inventory"] = new_inventory

    # =========================
    # FIX ROOM ITEMS
    # =========================
    room = get_room(player.get("room"))

    fixed_room = 0
    removed_room = 0

    if room and hasattr(room, "items"):

        new_items = []

        for item in room.items:

            # corretto
            if isinstance(item, dict) and isinstance(item.get("name"), str):
                new_items.append(item)
                continue

            # stringa → converti
            if isinstance(item, str):
                new_item = {
                    "name": item.replace(" ", "_"),
                    "display_name": item.title(),
                    "quantity": 1
                }
                new_items.append(new_item)
                fixed_room += 1
                continue

            # corrotto → elimina
            removed_room += 1

        room.items = new_items

    # =========================
    # OUTPUT
    # =========================
    conn.send("\n=== FIX ITEMS COMPLETATO ===\n")

    conn.send(f"Inventory: {fixed_inv} fixati, {removed_inv} rimossi\n")
    conn.send(f"Room: {fixed_room} fixati, {removed_room} rimossi\n\n")

    print(f"[FIX ITEMS] {player['name']} | inv_fix={fixed_inv} inv_rm={removed_inv} room_fix={fixed_room} room_rm={removed_room}")