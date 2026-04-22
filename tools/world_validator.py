import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ROOMS_DIR = os.path.join(BASE_DIR, "data", "rooms")
MOBS_DIR = os.path.join(BASE_DIR, "data", "mobs")
ITEMS_DIR = os.path.join(BASE_DIR, "data", "items")

START_ITEM_VNUM = 3000


# =========================
# UTILS
# =========================
def load_json_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERRORE JSON] {os.path.basename(path)} -> {e}")
        return None


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================
# ITEMS FIX
# =========================
def fix_items():

    print("\n=== FIX ITEMS ===")

    items = {}
    current_vnum = START_ITEM_VNUM

    for file in os.listdir(ITEMS_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(ITEMS_DIR, file)
        data = load_json_safe(path)

        if not data:
            continue

        # FIX vnum
        if "vnum" not in data:
            current_vnum += 1
            data["vnum"] = current_vnum
            print(f"[FIX] {file} -> vnum {current_vnum}")

        items[data["vnum"]] = data
        save_json(path, data)

    return items


# =========================
# MOBS FIX
# =========================
def fix_mobs():

    print("\n=== FIX MOBS ===")

    mobs = {}

    for file in os.listdir(MOBS_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(MOBS_DIR, file)
        data = load_json_safe(path)

        if not data:
            continue

        # campi base
        data.setdefault("name", file.replace(".json", ""))
        data.setdefault("hp", 10)
        data.setdefault("damage", 1)
        data.setdefault("defense", 0)
        data.setdefault("inventory", [])
        data.setdefault("loot", [])
        data.setdefault("xp", 10)

        mobs[data["name"].lower()] = data

        save_json(path, data)
        print(f"[OK] {data['name']}")

    return mobs


# =========================
# ROOMS FIX
# =========================
def fix_rooms(mobs, items):

    print("\n=== FIX ROOMS ===")

    for file in os.listdir(ROOMS_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(ROOMS_DIR, file)
        data = load_json_safe(path)

        if not data:
            continue

        # base
        data.setdefault("name", "Stanza")
        data.setdefault("description", "")
        data.setdefault("exits", {})
        data.setdefault("items", [])
        data.setdefault("mobs", [])

        # FIX EXITS
        for direction, exit_data in list(data["exits"].items()):

            if isinstance(exit_data, int):
                # 🔥 vecchio formato → nuovo
                data["exits"][direction] = {
                    "to": exit_data,
                    "door": False,
                    "closed": False,
                    "locked": False,
                    "key": None,
                    "secret": False
                }

            elif isinstance(exit_data, dict):
                exit_data.setdefault("to", None)
                exit_data.setdefault("door", False)
                exit_data.setdefault("closed", False)
                exit_data.setdefault("locked", False)
                exit_data.setdefault("key", None)
                exit_data.setdefault("secret", False)

        # FIX MOB RIFERIMENTI
        fixed_mobs = []
        for m in data["mobs"]:
            if m.lower() in mobs:
                fixed_mobs.append(m)
            else:
                print(f"[ERRORE] Mob non trovato: {m}")

        data["mobs"] = fixed_mobs

        # FIX ITEM RIFERIMENTI
        item_names = [i["name"] for i in items.values()]
        fixed_items = []

        for i in data["items"]:
            if i in item_names:
                fixed_items.append(i)
            else:
                print(f"[ERRORE] Item non trovato: {i}")

        data["items"] = fixed_items

        save_json(path, data)
        print(f"[OK] Room {data.get('vnum', '?')}")


# =========================
# MAIN
# =========================
def main():

    print("\n===== WORLD VALIDATOR =====")

    items = fix_items()
    mobs = fix_mobs()
    fix_rooms(mobs, items)

    print("\n✅ FIX COMPLETATO")


if __name__ == "__main__":
    main()