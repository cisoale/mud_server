import os
import json

# 🔥 BASE PATH CORRETTO
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ITEMS_DIR = os.path.join(BASE_DIR, "data", "items")

# 🔥 START VNUM
START_VNUM = 3000


def main():

    print("ITEMS_DIR:", ITEMS_DIR)

    current_vnum = START_VNUM

    for filename in os.listdir(ITEMS_DIR):

        if not filename.endswith(".json"):
            continue

        path = os.path.join(ITEMS_DIR, filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERRORE] {filename}: {e}")
            continue

        # 🔥 FIX VNUM
        if "vnum" not in data:

            current_vnum += 1
            data["vnum"] = current_vnum

            print(f"[FIX] {filename} -> vnum {current_vnum}")

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        else:
            print(f"[OK] {filename} già ha vnum {data['vnum']}")


if __name__ == "__main__":
    main()