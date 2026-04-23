from core.world import get_room
from core.inventory import add_item


def execute(player, conn, args):

    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    if not args:
        conn.send("Prendere cosa?\n")
        return

    search = args[0].lower()

    # =========================
    # 🔍 CERCA OGGETTO A TERRA
    # =========================
    for item in getattr(room, "items", []):

        if not isinstance(item, dict):
            continue

        name = item.get("name", "").lower()

        if (
            search in name
            or name in search
            or any(word in name for word in search.split())
        ):

            # =========================
            # 💰 GOLD (PRIORITARIO)
            # =========================
            if item.get("type") == "gold":

                amount = item.get("amount", 0)

                if amount <= 0:
                    room.items.remove(item)
                    conn.send("Non c'è nulla da raccogliere.\n")
                    return

                player["gold"] = player.get("gold", 0) + amount

                room.items.remove(item)

                conn.send(f"Raccogli {amount} monete.\n")
                return  # 🔥 IMPORTANTISSIMO

            # =========================
            # 🎒 OGGETTI NORMALI
            # =========================
            if add_item(player, item):
                room.items.remove(item)
                conn.send(f"Hai preso {name}.\n")
            else:
                conn.send("Sei troppo carico.\n")

            return

    # =========================
    # 🔍 CERCA NEI CONTENITORI (corpse)
    # =========================
    if len(args) > 1:

        container_search = " ".join(args[1:]).lower()

        for item in getattr(room, "items", []):

            if not isinstance(item, dict):
                continue

            if item.get("type") != "corpse":
                continue

            container_name = item.get("name", "").lower()

            if container_search in container_name:

                inventory = item.get("inventory", [])

                for obj in inventory:

                    if isinstance(obj, dict):
                        obj_name = obj.get("name", "").lower()
                    else:
                        obj_name = str(obj).lower()

                    if search in obj_name:

                        # 💰 GOLD dentro corpse (extra safe)
                        if isinstance(obj, dict) and obj.get("type") == "gold":

                            amount = obj.get("amount", 0)
                            player["gold"] = player.get("gold", 0) + amount

                            inventory.remove(obj)
                            conn.send(f"Raccogli {amount} monete da {container_name}.\n")
                            return

                        if add_item(player, obj):
                            inventory.remove(obj)
                            conn.send(f"Hai preso {obj_name} da {container_name}.\n")
                        else:
                            conn.send("Sei troppo carico.\n")

                        return

                conn.send("Oggetto non trovato nel contenitore.\n")
                return

    conn.send("Non trovi nulla.\n")