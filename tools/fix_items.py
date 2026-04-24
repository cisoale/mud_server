import os
import json
import shutil

ITEMS_DIR = "../data/items"
BACKUP_DIR = "../data/items_backup"


# =========================
# UTIL
# =========================
def safe_load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERRORE LOAD] {path}: {e}")
        return None


def safe_save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================
# NORMALIZE ITEM
# =========================
def normalize_item(data, filename):

    name = data.get("name", "").strip().lower()

    # 🔥 fix nome file vs nome interno
    if not name:
        name = filename.replace(".json", "")

    name = name.replace(" ", "_").replace(".", "")

    # display name
    display_name = data.get("display_name")

    if not display_name:
        display_name = name.replace("_", " ").title()

    # type
    item_type = data.get("type", "misc")

    # rarity
    rarity = data.get("rarity", "common")

    # consumable
    consumable = data.get("consumable", {})

    if "heal" in data:
        consumable["heal"] = data.get("heal", 0)

    if "mana" in data:
        consumable["mana"] = data.get("mana", 0)

    # slot
    slot = data.get("slot")

    # stats
    damage = data.get("damage", 0)
    defense = data.get("defense", 0)

    # value
    value = data.get("value", 10)

    # weight
    weight = data.get("weight", 1)

    # vnum
    vnum = data.get("vnum", 0)

    # =========================
    # COSTRUZIONE FINALE
    # =========================
    new_item = {
        "name": name,
        "display_name": display_name,
        "description": data.get("description", ""),

        "type": item_type,
        "rarity": rarity,

        "value": value,
        "weight": weight,
        "vnum": vnum
    }

    # aggiungi solo se utili
    if consumable:
        new_item["consumable"] = consumable

    if slot:
        new_item["slot"] = slot

    if damage:
        new_item["damage"] = damage

    if defense:
        new_item["defense"] = defense

    return new_item


# =========================
# MAIN
# =========================
def fix_items():

    print("=== FIX ITEMS START ===")

    # backup
    if not os.path.exists(BACKUP_DIR):
        shutil.copytree(ITEMS_DIR, BACKUP_DIR)
        print("[BACKUP] Creato backup completo")

    for file in os.listdir(ITEMS_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(ITEMS_DIR, file)

        data = safe_load(path)
        if not data:
            continue

        new_data = normalize_item(data, file)

        safe_save(path, new_data)

        print(f"[FIXED] {file}")

    print("=== FIX COMPLETED ===")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    fix_items()