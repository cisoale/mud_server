import os
import json

MOBS_DIR = "../data/mobs"
ITEMS_DIR = "../data/items"


# =========================
# LOAD ITEM NAMES
# =========================
def load_item_names():

    items = set()

    for file in os.listdir(ITEMS_DIR):
        if file.endswith(".json"):
            items.add(file.replace(".json", ""))

    return items


# =========================
# VALIDATE LOOT
# =========================
def validate_loot(mob, item_names):

    errors = []
    warnings = []

    for entry in mob.get("loot", []):

        item = entry.get("item")

        if not item:
            errors.append("loot senza item")
            continue

        if item not in item_names:
            errors.append(f"item inesistente: {item}")

        chance = entry.get("chance")

        if chance is None:
            errors.append(f"chance mancante per {item}")
        elif not (0 <= chance <= 1):
            errors.append(f"chance non valida ({item})")

        if "min" in entry and "max" in entry:
            if entry["min"] > entry["max"]:
                errors.append(f"min > max per {item}")

        rarity = entry.get("rarity")
        if rarity:
            valid = ["common", "uncommon", "rare", "epic", "legendary"]
            if rarity not in valid:
                warnings.append(f"rarity non valida ({item})")

    return errors, warnings


# =========================
# VALIDATE MOB
# =========================
def validate_mob(data, filename, item_names):

    errors = []
    warnings = []

    # =========================
    # BASE
    # =========================
    if not data.get("name"):
        errors.append("name mancante")

    if not data.get("vnum"):
        warnings.append("vnum mancante")

    # =========================
    # STATS
    # =========================
    if data.get("hp", 0) <= 0:
        errors.append("hp non valido")

    if data.get("damage", 0) < 0:
        errors.append("damage negativo")

    if data.get("xp", 0) < 0:
        errors.append("xp negativo")

    # =========================
    # GOLD
    # =========================
    gmin = data.get("gold_min", 0)
    gmax = data.get("gold_max", 0)

    if gmin > gmax:
        errors.append("gold_min > gold_max")

    # =========================
    # TYPE
    # =========================
    mob_type = data.get("type", "normal")

    valid_types = ["normal", "elite", "boss"]

    if mob_type not in valid_types:
        warnings.append(f"type non valido ({mob_type})")

    # =========================
    # LOOT
    # =========================
    loot_errors, loot_warnings = validate_loot(data, item_names)

    errors.extend(loot_errors)
    warnings.extend(loot_warnings)

    # =========================
    # LUA SCRIPT
    # =========================
    script = data.get("loot_script")

    if script:
        if not os.path.exists(os.path.join("..", script)):
            warnings.append(f"loot_script non trovato ({script})")

    return errors, warnings


# =========================
# MAIN
# =========================
def validate_mobs():

    print("=== VALIDAZIONE MOBS ===\n")

    item_names = load_item_names()

    total = 0
    total_errors = 0
    total_warnings = 0

    for file in os.listdir(MOBS_DIR):

        if not file.endswith(".json"):
            continue

        total += 1

        path = os.path.join(MOBS_DIR, file)

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[CRASH] {file}: {e}")
            total_errors += 1
            continue

        errors, warnings = validate_mob(data, file, item_names)

        if errors or warnings:

            print(f"\n[{file}]")

            for e in errors:
                print(f"  ❌ ERRORE: {e}")
                total_errors += 1

            for w in warnings:
                print(f"  ⚠️ WARNING: {w}")
                total_warnings += 1

    print("\n=========================")
    print(f"Totale mobs: {total}")
    print(f"Errori: {total_errors}")
    print(f"Warning: {total_warnings}")
    print("=========================")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    validate_mobs()