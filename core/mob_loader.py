import json
import os

# =========================
# STORAGE MOB
# =========================
MOBS = {}


# =========================
# LOAD MOBS
# =========================
def load_mobs():
    global MOBS
    MOBS = {}

    base_path = os.path.join(os.getcwd(), "data", "mobs")

    if not os.path.exists(base_path):
        print("[MOBS] Cartella non trovata")
        return

    print("[MOBS] Caricamento...")

    for file in os.listdir(base_path):

        if not file.endswith(".json"):
            continue

        path = os.path.join(base_path, file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

                name = data.get("name", "").lower()

                if not name:
                    print(f"[ERRORE] Nome mancante in {file}")
                    continue

                # valori base
                data.setdefault("max_hp", 20)
                data.setdefault("hp", data["max_hp"])
                data.setdefault("xp", 10)
                data.setdefault("inventory", [])

                MOBS[name] = data

                print(f"[OK] {name}")

        except Exception as e:
            print(f"[ERRORE] {file}: {e}")

    print(f"[MOBS] Totale: {len(MOBS)}\n")


# =========================
# GET MOB TEMPLATE
# =========================
def get_mob_template(name):

    if not name:
        return None

    name = name.lower()

    # match diretto
    if name in MOBS:
        return MOBS[name]

    # match parziale
    for mob_name, mob in MOBS.items():
        if name in mob_name:
            return mob

    return None


# =========================
# DEBUG
# =========================
def list_mobs():
    return list(MOBS.keys())