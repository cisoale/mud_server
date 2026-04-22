import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ITEMS_DIR = os.path.join(BASE_DIR, "data", "items")
MOBS_DIR = os.path.join(BASE_DIR, "data", "mobs")

# 🔥 RANGE SEPARATI (IMPORTANTISSIMO)
ITEM_START = 3000
MOB_START = 2000


# =========================
# UTILS
# =========================
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERRORE JSON] {path}: {e}")
        return None


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================
# GENERATORE VNUM SICURO
# =========================
def get_next_vnum(existing, start):
    v = start
    while v in existing:
        v += 1
    return v


# =========================
# FIX GENERICO
# =========================
def fix_directory(directory, start_vnum, label):

    print(f"\n=== FIX {label.upper()} ===")

    used_vnums = set()
    files_data = []

    # 🔹 prima passata → raccoglie vnum esistenti
    for file in os.listdir(directory):

        if not file.endswith(".json"):
            continue

        path = os.path.join(directory, file)
        data = load_json(path)

        if not data:
            continue

        vnum = data.get("vnum")

        if isinstance(vnum, int):
            used_vnums.add(vnum)

        files_data.append((file, path, data))

    # 🔹 seconda passata → assegna mancanti
    for file, path, data in files_data:

        if "vnum" not in data or not isinstance(data["vnum"], int):

            new_vnum = get_next_vnum(used_vnums, start_vnum)
            data["vnum"] = new_vnum
            used_vnums.add(new_vnum)

            print(f"[FIX] {label} {file} -> vnum {new_vnum}")

            save_json(path, data)

        else:
            print(f"[OK] {label} {file} -> {data['vnum']}")


# =========================
# MAIN
# =========================
def main():

    print("\n===== AUTO VNUM TOOL =====")

    fix_directory(MOBS_DIR, MOB_START, "mob")
    fix_directory(ITEMS_DIR, ITEM_START, "item")

    print("\n✅ COMPLETATO")


if __name__ == "__main__":
    main()