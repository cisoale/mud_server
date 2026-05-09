import os
import json
import copy

MOBS = {}


# =========================
# STANDARD MOB STRUCTURE
# =========================
STANDARD_MOB = {
    "name": "mob",
    "description": "",
    "level": 1,

    "hp": 10,
    "current_hp": None,

    "damage": 1,
    "defense": 0,

    "xp": 10,

    # loot system
    "inventory": [],
    "loot": [],

    # gold system
    "gold_min": 0,
    "gold_max": 0,

    # combat
    "target": None,

    # events
    "death_events": [],

    # id
    "vnum": None
}


# =========================
# NORMALIZE MOB
# =========================
def normalize_mob(data):
    """
    Garantisce che ogni mob abbia tutti i campi necessari.
    Non rompe i vecchi mob.
    """

    mob = copy.deepcopy(STANDARD_MOB)

    # merge dati
    for key, value in data.items():
        mob[key] = value

    # runtime fields
    mob["current_hp"] = mob.get("hp", 10)

    # sicurezza liste
    mob["inventory"] = list(mob.get("inventory", []))
    mob["loot"] = list(mob.get("loot", []))
    mob["death_events"] = list(mob.get("death_events", []))

    # retrocompatibilità: usa inventory come loot se manca
    if not mob["loot"] and mob["inventory"]:
        mob["loot"] = mob["inventory"]

    return mob


# =========================
# LOAD MOBS
# =========================
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

                # salva template RAW (non normalizzato)
                MOBS[name] = data

                if vnum:
                    MOBS[str(vnum)] = data

                print(f"[OK] {name}")

            except Exception as e:
                print(f"[ERRORE JSON] {file}: {e}")

    print(f"[MOBS] Totale: {len(MOBS)}")


# =========================
# GET MOB TEMPLATE
# =========================
def get_mob(key):
    if not key:
        return None
    return MOBS.get(str(key).lower())


# =========================
# CREATE MOB INSTANCE
# =========================
def create_mob(key):
    print(
      f"[LEGACY MOB LOADER] "
      f"create_mob chiamato"
    )
    """
    Crea una copia runtime del mob con struttura completa.
    """

    template = get_mob(key)

    if not template:
        return None

    # 🔥 NORMALIZZAZIONE QUI
    mob = normalize_mob(template)

    return mob