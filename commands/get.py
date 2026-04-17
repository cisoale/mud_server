from core.world import get_room
from core.inventory import add_item


def execute(player, conn, command, args):

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

                        if add_item(player, obj):
                            inventory.remove(obj)
                            conn.send(f"Hai preso {obj_name} da {container_name}.\n")
                        else:
                            conn.send("Sei troppo carico.\n")

                        return

                conn.send("Oggetto non trovato nel contenitore.\n")
                return

    conn.send("Non trovi nulla.\n")