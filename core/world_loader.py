import os
import json
from core.world import add_room
from core.world_validator import validate_and_fix_room
from core.mob_factory import create_mob

ROOMS_PATH = "data/rooms"


def load_rooms_from_files():

    print("[WORLD] Caricamento rooms...")

    for filename in os.listdir(ROOMS_PATH):

        if not filename.endswith(".json"):
            continue

        path = os.path.join(ROOMS_PATH, filename)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 🔥 VALIDATOR
        data, changed = validate_and_fix_room(data)

        if changed:
            print(f"[FIX] Room {data.get('vnum')} corretta automaticamente")

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        # =========================
        # 🔥 FIX QUI
        # =========================
        vnum = data.get("vnum")
        name = data.get("name", "Stanza")
        desc = data.get("description", "")

        if not vnum:
            print(f"[ERRORE] Room senza vnum: {filename}")
            continue

        room = add_room(vnum, name, desc)

        # coordinate
        room.x = data.get("x", 100)
        room.y = data.get("y", 100)

        # exits
        room.exits = data.get("exits", {})

        # mobs
        room.mobs = []

        for mob_name in data.get("mobs", []):
            template = get_mob_template(mob_name.lower())

            if not template:
              print(f"[ERRORE] Mob non trovato: {mob_name}")
              continue

            mob = create_mob(mob_name)
            room.mobs.append(mob)
        # items
        room.items = data.get("items", [])

        print(f"[OK] Room {vnum}")

    print("[WORLD] Caricamento completato.\n")