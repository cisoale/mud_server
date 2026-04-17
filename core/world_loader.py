import os
import json

from core.world import add_room

ROOMS_PATH = "data/rooms"


def load_rooms_from_files():

    print("[WORLD] Caricamento rooms...")

    for file in os.listdir(ROOMS_PATH):

        if not file.endswith(".json"):
            continue

        path = os.path.join(ROOMS_PATH, file)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        vnum = data["vnum"]
        name = data.get("name", "Room")
        desc = data.get("description", "")

        # ✅ CREA OGGETTO ROOM
        room = add_room(vnum, name, desc)

        # exits
        room.exits = data.get("exits", {})

        # sempre liste pulite
        room.players = []
        room.mobs = []
        room.items = []

        print(f"[OK] Room {vnum}")

    print("[WORLD] Caricamento completato.\n")