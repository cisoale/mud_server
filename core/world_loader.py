import os
import json

from core.world import add_room, get_room
from core.world_validator import validate_and_fix_room

# TEMPLATE LOADER
from core.mob_loader import get_mob

# ECS FACTORY
from core.mob_factory import create_mob

ROOMS_PATH = "data/rooms"


# =====================================
# STATIC NPCS
# =====================================

def load_static_npcs():

    # =========================
    # LOCANDIERE
    # =========================

    room = get_room(1001)

    if not room:

        print("[NPC] Room 1001 non trovata")

        return

    # TEMPLATE
    template = get_mob("locandiere")

    if not template:

        print("[NPC] locandiere non trovato")

        return

    # ECS NPC
    npc = create_mob(template)

    room.mobs.append(npc)

    npc["room"] = room.vnum

    # POSITION COMPONENT
    position = npc["components"].get(
        "PositionComponent"
    )

    if position:
        position.room_id = room.vnum

    # DEBUG ECS
    print(
        f"[ECS NPC] {npc['name']} -> "
        f"{list(npc['components'].keys())}"
    )

    print(
        "[NPC] locandiere "
        "spawnato in room 1001"
    )


# =====================================
# LOAD ROOMS
# =====================================

def load_rooms_from_files():

    print("[WORLD] Caricamento rooms...")

    if not os.path.exists(ROOMS_PATH):

        print(
            f"[ERRORE] "
            f"Cartella rooms non trovata: "
            f"{ROOMS_PATH}"
        )

        return

    for filename in os.listdir(ROOMS_PATH):

        if filename == "roomModel.json":
            continue

        if not filename.endswith(".json"):
            continue

        path = os.path.join(
            ROOMS_PATH,
            filename
        )

        # =========================
        # LOAD JSON
        # =========================

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

        except Exception as e:

            print(
                f"[ERRORE] "
                f"Lettura {filename}: {e}"
            )

            continue

        # =========================
        # VALIDAZIONE
        # =========================

        data, changed = validate_and_fix_room(
            data
        )

        if changed:

            print(
                f"[FIX] Room "
                f"{data.get('vnum')} "
                f"corretta automaticamente"
            )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    data,
                    f,
                    indent=4
                )

        # =========================
        # BASE DATA
        # =========================

        vnum = data.get("vnum")

        name = data.get(
            "name",
            "Stanza"
        )

        desc = data.get(
            "description",
            ""
        )

        # =========================
        # REGION
        # =========================

        region = data.get(
            "region",
            "starting_region"
        )

        print(region)

        if not vnum:

            print(
                f"[ERRORE] "
                f"Room senza vnum: "
                f"{filename}"
            )

            continue

        # =========================
        # ROOM CREATION
        # =========================

        room = add_room(
            vnum,
            name,
            desc,
            region
        )

        print(
            f"[REGION] "
            f"Room {vnum} -> "
            f"{room.region_id}"
        )

        # =========================
        # POSITION
        # =========================

        room.x = data.get("x", 100)

        room.y = data.get("y", 100)

        # =========================
        # EXITS
        # =========================

        room.exits = data.get(
            "exits",
            {}
        )

        # =========================
        # ECS MOBS
        # =========================

        room.mobs = []

        for mob_name in data.get(
            "mobs",
            []
        ):

            # TEMPLATE
            template = get_mob(mob_name)

            if not template:

                print(
                    f"[WARN] "
                    f"Mob non trovato: "
                    f"{mob_name}"
                )

                continue

            # ECS MOB
            mob = create_mob(template)

            if not mob:
                continue

            room.mobs.append(mob)

            mob["room"] = room.vnum

            # POSITION COMPONENT
            position = mob["components"].get(
                "PositionComponent"
            )

            if position:
                position.room_id = room.vnum

            # DEBUG ECS
            print(
                f"[ECS ROOM MOB] "
                f"{mob['name']} -> "
                f"{list(mob['components'].keys())}"
            )

        # =========================
        # ITEMS
        # =========================

        room.items = data.get(
            "items",
            []
        )

        print(
            f"[OK] Room {vnum} caricata"
        )

    print(
        "[WORLD] "
        "Caricamento completato.\n"
    )