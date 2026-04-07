import json
import os
from core.world import Room, rooms
from core.mob_loader import mobs_data
from core.mob_factory import create_mob


def load_rooms_from_files():
    folder = "data/rooms"

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            vnum = data.get("vnum")
            name = data.get("name", f"Room {vnum}")
            desc = data.get("description", "")
            exits = data.get("exits", {})

            if not vnum:
                print(f"[ERRORE] vnum mancante in {file}")
                continue

            room = Room(vnum, name, desc, exits)

            # 👹 SPAWN MOB (QUI DENTRO!)
            for mob_name in data.get("mobs", []):
                mob_data = mobs_data.get(mob_name)

                if not mob_data:
                    print(f"[ERRORE] mob non trovato: {mob_name}")
                    continue

                mob = create_mob(
                    mob_data["name"],
                    mob_data.get("description", ""),
                    mob_data.get("hp", 10),
                    mob_data.get("inventory", []),
                    mob_data.get("xp", 10)
                )

                room.mobs.append(mob)

            rooms[vnum] = room

        except Exception as e:
            print(f"[ERRORE] Caricamento {file}: {e}")