import json
import os

ITEMS = {}

def load_items():
    global ITEMS
    ITEMS = {}

    base_path = os.path.join(os.getcwd(), "data", "items")

    if not os.path.exists(base_path):
        print("[ITEMS] Cartella items non trovata.")
        return

    print("[ITEMS] Caricamento...")

    for file in os.listdir(base_path):

        if not file.endswith(".json"):
            continue

        path = os.path.join(base_path, file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

                name = data.get("name", "").lower()

                if not name:
                    continue

                data.setdefault("weight", 1)

                ITEMS[name] = data

                print(f"[OK] Item caricato: {name}")

        except Exception as e:
            print(f"[ERRORE ITEM] {file}: {e}")

    print(f"[ITEMS] Totale: {len(ITEMS)}\n")


def get_item_template(name):

    name = name.lower()

    if name in ITEMS:
        return ITEMS[name]

    for item_name, item in ITEMS.items():
        if name in item_name:
            return item

    return None