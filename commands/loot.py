from core.world import get_room
from core.inventory import add_item


def execute(player, conn, command, args):

    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    if not args:
        conn.send("Loot cosa?\n")
        return

    items = getattr(room, "items", [])

    # =========================
    # 🔢 LOOT PER NUMERO
    # =========================
    if args[0].isdigit():

        index = int(args[0]) - 1

        if index < 0 or index >= len(items):
            conn.send("Indice non valido.\n")
            return

        target = items[index]

        if not isinstance(target, dict) or target.get("type") != "corpse":
            conn.send("Non puoi lootare quello.\n")
            return

        inventory = target.get("inventory", [])

        if not inventory:
            conn.send("Il corpo è vuoto.\n")
            return

        taken = []
        remaining = []

        for obj in inventory:

            name = obj.get("name", "oggetto") if isinstance(obj, dict) else str(obj)

            if add_item(player, obj):
                taken.append(name)
            else:
                remaining.append(obj)
                conn.send(f"Non puoi prendere {name} (troppo peso).\n")

        target["inventory"] = remaining

        if taken:
            conn.send("Hai preso:\n")
            for t in taken:
                conn.send(f"- {t}\n")
        else:
            conn.send("Non riesci a prendere nulla.\n")

        return

    # =========================
    # 🔍 RICERCA INTELLIGENTE CORPO
    # =========================
    search = " ".join(args).lower()
    target = None

    for item in items:

        if not isinstance(item, dict):
            continue

        name = item.get("name", "").lower()

        if item.get("type") == "corpse":
            if (
                search in name
                or name in search
                or any(word in name for word in search.split())
            ):
                target = item
                break

    if not target:
        conn.send("Non trovi nulla da lootare.\n")
        return

    inventory = target.get("inventory", [])

    if not inventory:
        conn.send("Il corpo è vuoto.\n")
        return

    # =========================
    # 👜 LOOT TUTTO
    # =========================
    if len(args) == 1:

        taken = []
        remaining = []

        for obj in inventory:

            name = obj.get("name", "oggetto") if isinstance(obj, dict) else str(obj)

            if add_item(player, obj):
                taken.append(name)
            else:
                remaining.append(obj)
                conn.send(f"Non puoi prendere {name} (troppo peso).\n")

        target["inventory"] = remaining

        if taken:
            conn.send("Hai preso:\n")
            for t in taken:
                conn.send(f"- {t}\n")
        else:
            conn.send("Non riesci a prendere nulla.\n")

        return

    # =========================
    # 🎯 LOOT SINGOLO OGGETTO
    # =========================
    item_search = " ".join(args[1:]).lower()

    for obj in inventory:

        name = obj.get("name", "").lower() if isinstance(obj, dict) else str(obj).lower()

        if item_search in name:

            if add_item(player, obj):
                inventory.remove(obj)
                conn.send(f"Prendi {name}.\n")
            else:
                conn.send("Sei troppo carico.\n")

            return

    conn.send("Oggetto non trovato nel corpo.\n")