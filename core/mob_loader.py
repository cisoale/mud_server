import os
import json

MOBS = {}


def load_mobs():

    global MOBS
    MOBS = {}

    path = "data/mobs"

    print("\n[MOBS] Caricamento...")

    for file in os.listdir(path):

        if not file.endswith(".json"):
            continue

        with open(os.path.join(path, file), encoding="utf-8") as f:
            try:
                data = json.load(f)

                name = data.get("name", "").lower()
                vnum = data.get("vnum")

                if not name:
                    print(f"[ERRORE] Mob senza nome: {file}")
                    continue

                MOBS[name] = data

                if vnum:
                    MOBS[str(vnum)] = data

                print(f"[OK] {name}")

            except Exception as e:
                print(f"[ERRORE JSON] {file}: {e}")

    print(f"[MOBS] Totale: {len(MOBS)}")


def get_mob(key):
    return MOBS.get(key.lower())


def create_mob(key):

    template = get_mob(key)

    if not template:
        return None

    # copia per evitare modifiche globali
    mob = dict(template)

    mob["current_hp"] = mob.get("hp", 10)
    mob["inventory"] = mob.get("inventory", [])

    return mob