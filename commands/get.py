from core.world import get_room
from core.item_utils import add_item


def execute(player, conn, args):

    room = get_room(player.get("room"))

    if not room:
        conn.send("Errore stanza.\n")
        return

    if not args:
        conn.send("Prendere cosa?\n")
        return

    inventory = player.setdefault("inventory", [])

    # =========================
    # GET ALL
    # =========================
    if args[0].lower() == "all":

        if not getattr(room, "items", []):
            conn.send("Non c'è nulla da raccogliere.\n")
            return

        picked = 0

        for item in list(room.items):

            if add_item(inventory, item):
                room.items.remove(item)
                picked += 1

        conn.send("Raccogli tutto.\n" if picked else "Nulla da raccogliere.\n")
        return

    # =========================
    # GET SINGOLO
    # =========================
    search = " ".join(args).lower()

    for item in list(getattr(room, "items", [])):

        if not isinstance(item, dict):
            continue

        name = item.get("name", "").lower()

        if search in name:

            # GOLD
            if item.get("type") == "gold":
                amount = item.get("amount", 0)
                player["gold"] = player.get("gold", 0) + amount
                room.items.remove(item)
                conn.send(f"Raccogli {amount} monete.\n")
                return

            # ITEM
            if add_item(inventory, item):
                room.items.remove(item)
                conn.send(f"Hai preso {item.get('display_name', name)}.\n")
            else:
                conn.send("Sei troppo carico.\n")

            return

    conn.send("Non trovi nulla.\n")