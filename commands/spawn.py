from core.mob_loader import get_mob
from core.mob_factory import create_mob

from core.item_loader import create_item

from core.world import get_room


# =====================================
# SPAWN COMMAND
# =====================================

def execute(player, conn, args):

    if not args:

        conn.send(
            "Uso:\n"
            "spawn mob <nome>\n"
            "spawn item <nome>\n"
        )

        return

    # =================================
    # ROOM
    # =================================

    room = get_room(
        player.get("room")
    )

    if not room:

        conn.send(
            "Room non trovata.\n"
        )

        return

    # =================================
    # TYPE
    # =================================

    spawn_type = args[0].lower()

    # =================================
    # MOB
    # =================================

    if spawn_type == "mob":

        if len(args) < 2:

            conn.send(
                "Spawn quale mob?\n"
            )

            return

        target = " ".join(args[1:])

        # =============================
        # TEMPLATE
        # =============================

        template = get_mob(target)

        if not template:

            conn.send(
                "Mob non trovato.\n"
            )

            return

        # =============================
        # ECS RUNTIME MOB
        # =============================

        mob = create_mob(template)

        if not mob:

            conn.send(
                "Errore creazione mob.\n"
            )

            return

        # room
        room.mobs.append(mob)

        mob["room"] = room.vnum

        # ECS PositionComponent
        position = mob["components"].get(
            "PositionComponent"
        )

        if position:
            position.room_id = room.vnum

        # DEBUG
        print(
            f"[ECS SPAWN COMMAND] "
            f"{mob['name']} -> "
            f"{list(mob['components'].keys())}"
        )

        conn.send(
            f"{mob['name']} "
            f"spawnato.\n"
        )

        return

    # =================================
    # ITEM
    # =================================

    elif spawn_type == "item":

        if len(args) < 2:

            conn.send(
                "Spawn quale item?\n"
            )

            return

        target = " ".join(args[1:])

        item = create_item(target)

        if not item:

            conn.send(
                "Item non trovato.\n"
            )

            return

        room.items.append(item)

        conn.send(
            f"{item['name']} "
            f"spawnato.\n"
        )

        return

    # =================================
    # UNKNOWN
    # =================================

    conn.send(
        "Tipo spawn non valido.\n"
    )