import os
import json

ITEMS_DIR = "../data/items"


# =========================
# VALIDATOR
# =========================
def validate_item(data, filename):

    errors = []
    warnings = []

    # =========================
    # NAME
    # =========================
    name = data.get("name")

    if not name:
        errors.append("name mancante")
    else:
        if " " in name or "." in name:
            errors.append("name non valido (usa snake_case)")

    # =========================
    # DISPLAY NAME
    # =========================
    if not data.get("display_name"):
        warnings.append("display_name mancante")

    # =========================
    # TYPE
    # =========================
    item_type = data.get("type")

    valid_types = ["weapon", "armor", "consumable", "misc"]

    if item_type not in valid_types:
        warnings.append(f"type non valido ({item_type})")

    # =========================
    # RARITY
    # =========================
    rarity = data.get("rarity", "common")

    valid_rarity = ["common", "uncommon", "rare", "epic", "legendary"]

    if rarity not in valid_rarity:
        warnings.append(f"rarity non valida ({rarity})")

    # =========================
    # SLOT (se equip)
    # =========================
    if item_type in ["weapon", "armor"]:

        if not data.get("slot"):
            errors.append("slot mancante per item equip")

    # =========================
    # CONSUMABLE
    # =========================
    if item_type == "consumable":

        consumable = data.get("consumable")

        if not consumable:
            errors.append("consumable mancante")

        else:
            if not isinstance(consumable, dict):
                errors.append("consumable non è dict")

    # =========================
    # STATS
    # =========================
    if "damage" in data and not isinstance(data["damage"], int):
        errors.append("damage non è int")

    if "defense" in data and not isinstance(data["defense"], int):
        errors.append("defense non è int")

    # =========================
    # WEIGHT
    # =========================
    if "weight" in data and data["weight"] < 0:
        errors.append("weight negativo")

    return errors, warnings


# =========================
# MAIN
# =========================
def validate_items():

    print("=== VALIDAZIONE ITEMS ===\n")

    total = 0
    total_errors = 0
    total_warnings = 0

    for file in os.listdir(ITEMS_DIR):

        if not file.endswith(".json"):
            continue

        total += 1

        path = os.path.join(ITEMS_DIR, file)

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[CRASH] {file}: {e}")
            total_errors += 1
            continue

        errors, warnings = validate_item(data, file)

        if errors or warnings:

            print(f"\n[{file}]")

            for e in errors:
                print(f"  ❌ ERRORE: {e}")
                total_errors += 1

            for w in warnings:
                print(f"  ⚠️ WARNING: {w}")
                total_warnings += 1

    print("\n=========================")
    print(f"Totale file: {total}")
    print(f"Errori: {total_errors}")
    print(f"Warning: {total_warnings}")
    print("=========================")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    validate_items()