from core.world import get_room, broadcast_room
from core.item_utils import add_item


def execute(player, conn, args):

    if not args:
        conn.send("Lasciare cosa?\n")
        return

    room = get_room(player.get("room"))
    if not room:
        conn.send("Errore stanza.\n")
        return

    inventory = player.get("inventory", [])

    # =========================
    # DROP ALL
    # =========================
    if args[0].lower() == "all":

        if len(args) < 2 or args[1].lower() != "yes":
            conn.send("Sei sicuro? Scrivi: drop all yes\n")
            return

        if not inventory:
            conn.send("Non hai nulla.\n")
            return

        for item in list(inventory):
            add_item(room.items, item)
            inventory.remove(item)

        conn.send("Hai lasciato tutto a terra.\n")

        broadcast_room(
            room,
            f"{player['name']} lascia tutto a terra.\n",
            exclude=player
        )
        return

    # =========================
    # DROP X (quantità)
    # =========================
    amount = None
    search = ""

    # es: drop 2 potion
    if args[0].isdigit():
        amount = int(args[0])
        search = " ".join(args[1:]).lower()
    else:
        search = " ".join(args).lower()

    for item in list(inventory):

        name = item.get("name", "").lower()

        if search in name:

            qty = item.get("quantity", 1)

            # =========================
            # DROP PARZIALE
            # =========================
            if amount and item.get("stackable"):

                if amount >= qty:
                    add_item(room.items, item)
                    inventory.remove(item)

                    conn.send(f"Hai lasciato tutto ({qty}) {item.get('display_name', name)}.\n")

                else:
                    item["quantity"] -= amount

                    dropped = item.copy()
                    dropped["quantity"] = amount

                    add_item(room.items, dropped)

                    conn.send(f"Hai lasciato {amount} {item.get('display_name', name)}.\n")

                broadcast_room(
                    room,
                    f"{player['name']} lascia {amount} {item.get('display_name', name)}.\n",
                    exclude=player
                )
                return

            # =========================
            # DROP NORMALE
            # =========================
            add_item(room.items, item)
            inventory.remove(item)

            conn.send(f"Hai lasciato {item.get('display_name', name)}.\n")

            broadcast_room(
                room,
                f"{player['name']} lascia {item.get('display_name', name)}.\n",
                exclude=player
            )
            return

    conn.send("Non hai quell'oggetto.\n")