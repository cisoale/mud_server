import os
import json

from core.world import add_room, get_room
from core.world_validator import validate_and_fix_room
from core.mob_loader import create_mob

ROOMS_PATH = "data/rooms"


def load_static_npcs():

    # =========================
    # LOCANDIERE
    # =========================
    room = get_room(1001)

    if not room:
        print("[NPC] Room 1001 non trovata")
        return

    npc = create_mob("locandiere")

    if not npc:
        print("[NPC] locandiere non trovato")
        return

    room.mobs.append(npc)
    npc["room"] = room.vnum

    print("[NPC] locandiere spawnato in room 1001")


def load_rooms_from_files():

    print("[WORLD] Caricamento rooms...")

    if not os.path.exists(ROOMS_PATH):
        print(f"[ERRORE] Cartella rooms non trovata: {ROOMS_PATH}")
        return

    for filename in os.listdir(ROOMS_PATH):

        if filename == "roomModel.json":
            continue
        if not filename.endswith(".json"):
            continue

        path = os.path.join(ROOMS_PATH, filename)

        # =========================
        # LOAD JSON SICURO
        # =========================
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

        except Exception as e:
            print(f"[ERRORE] Lettura {filename}: {e}")
            continue

        # =========================
        # VALIDAZIONE
        # =========================
        data, changed = validate_and_fix_room(data)

        if changed:

            print(f"[FIX] Room {data.get('vnum')} corretta automaticamente")

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
                pint(data)

        # =========================
        # DATI BASE
        # =========================
        vnum = data.get("vnum")
        name = data.get("name", "Stanza")
        desc = data.get("description", "")

        # =========================
        # REGION SYSTEM
        # =========================
        region = data.get("region", "starting_region")
        print(region)

        if not vnum:
            print(f"[ERRORE] Room senza vnum: {filename}")
            continue

        # =========================
        # CREAZIONE ROOM
        # =========================
        room = add_room(vnum, name, desc, region)

        print(f"[REGION] Room {vnum} -> {room.region_id}")

        # =========================
        # POSIZIONE
        # =========================
        room.x = data.get("x", 100)
        room.y = data.get("y", 100)

        # =========================
        # EXITS
        # =========================
        room.exits = data.get("exits", {})

        # =========================
        # MOB SPAWN AUTOMATICO
        # =========================
        room.mobs = []

        for mob_name in data.get("mobs", []):

            mob = create_mob(mob_name)

            if mob:
                room.mobs.append(mob)
            else:
                print(f"[WARN] Mob non trovato: {mob_name}")

        # =========================
        # ITEMS
        # =========================
        room.items = data.get("items", [])

        print(f"[OK] Room {vnum} caricata")

    print("[WORLD] Caricamento completato.\n")