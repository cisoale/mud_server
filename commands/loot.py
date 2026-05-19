from core.world import get_room
from core.item_loader import create_item
from core.save_system import save_player

# =========================================
# FIND CORPSE
# =========================================

def find_corpse(room, target_name):

    if not hasattr(room, "items"):
        return None

    target_name = str(
        target_name
    ).lower().strip()

    for item in room.items:

        if not isinstance(item, dict):
            continue

        item_name = str(
            item.get("name", "")
        ).lower()

        if not item_name.startswith("corpo"):
            continue

        # match diretto
        if target_name == item_name:
            return item

        # match parziale
        if target_name in item_name:
            return item

        # alias
        if target_name in [
            "corpo",
            "corpse"
        ]:
            return item

    return None


# =========================================
# LOOT COMMAND
# =========================================

def execute(player, conn, args):

    try:

        # =====================================
        # INPUT
        # =====================================

        if not args:

            conn.send(
                "Loot cosa?\n"
            )

            return

        if isinstance(args, list):

            target_name = " ".join(
                [str(x) for x in args]
            ).lower()

        else:

            target_name = str(
                args
            ).lower()

        # =====================================
        # ROOM
        # =====================================

        room = get_room(
            player.get("room")
        )

        if not room:

            conn.send(
                "La stanza non esiste.\n"
            )

            return

        # =====================================
        # CORPSE
        # =====================================

        corpse = find_corpse(
            room,
            target_name
        )

        if not corpse:

            conn.send(
                "Non trovi quel corpo.\n"
            )

            return

        looted_anything = False

        # =====================================
        # GOLD
        # =====================================

        gold = corpse.get(
            "gold",
            0
        )

        if isinstance(gold, int):

            if gold > 0:

                player["gold"] = (
                    player.get(
                        "gold",
                        0
                    ) + gold
                )
                save_player(player)
                conn.send(
                    f"Raccogli "
                    f"{gold} monete "
                    f"dal "
                    f"{corpse['name']}.\n"
                )

                corpse["gold"] = 0

                looted_anything = True

        # =====================================
        # ITEMS
        # =====================================

        loot_table = corpse.get(
            "loot",
            []
        )

        if not isinstance(
            loot_table,
            list
        ):
            loot_table = []

        for loot_entry in loot_table:

            if not isinstance(
                loot_entry,
                dict
            ):
                continue

            item_name = loot_entry.get(
                "item"
            )

            if not item_name:
                continue

            item = create_item(
                item_name
            )

            if not item:
                continue

            player.setdefault(
                "inventory",
                []
            ).append(item)

            conn.send(
                f"Trovi "
                f"{item['name']} "
                f"nel "
                f"{corpse['name']}.\n"
            )

            looted_anything = True

        # svuota loot
        corpse["loot"] = []

        # =====================================
        # EMPTY
        # =====================================

        if not looted_anything:

            conn.send(
                "Il corpo è vuoto.\n"
            )

            return

        # =====================================
        # REMOVE CORPSE
        # =====================================

        empty_gold = (
            corpse.get(
                "gold",
                0
            ) <= 0
        )

        empty_loot = not corpse.get(
            "loot",
            []
        )

        if empty_gold and empty_loot:

            if corpse in room.items:

                room.items.remove(
                    corpse
                )

                conn.send(
                    f"{corpse['name']} "
                    f"si dissolve lentamente.\n"
                )

    except Exception as e:

        print(
            f"[LOOT ERROR] {e}"
        )

        conn.send(
            "Errore comando.\n"
        )