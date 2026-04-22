from core.world import get_room
from core.inventory import remove_item


def execute(player, conn, args):

    if not args:
        conn.send("Drop cosa?\n")
        return

    search = " ".join(args).lower()

    inventory = player.get("inventory", [])

    target = None

    # =========================
    # 🔍 MATCH INTELLIGENTE
    # =========================
    for item in inventory:

        if isinstance(item, dict):
            name = item.get("name", "").lower()
        else:
            name = str(item).lower()

        if (
            search in name
            or name in search
            or any(word in name for word in search.split())
        ):
            target = item
            break

    if not target:
        conn.send("Non ce l'hai.\n")
        return

    # =========================
    # RIMUOVI DALL'INVENTARIO
    # =========================
    inventory.remove(target)

    room = get_room(player["room"])

    if not hasattr(room, "items"):
        room.items = []

    room.items.append(target)

    name = target.get("name") if isinstance(target, dict) else str(target)

    conn.send(f"Hai lasciato {name}.\n")