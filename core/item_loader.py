import os
import json

ITEMS = {}


# =========================
# LOAD ITEMS
# =========================
def load_items():

    global ITEMS
    ITEMS = {}

    path = "data/items"

    print("\n[ITEMS] Caricamento...")

    if not os.path.exists(path):
        print("[ERRORE] Cartella items non trovata:", path)
        return

    for file in os.listdir(path):

        if not file.endswith(".json"):
            continue

        full_path = os.path.join(path, file)

        try:
            with open(full_path, encoding="utf-8") as f:
                data = json.load(f)

            name = data.get("name", "").lower()
            vnum = data.get("vnum")

            if not name:
                print(f"[ERRORE] Item senza nome: {file}")
                continue

            # =========================
            # NORMALIZZAZIONE BASE
            # =========================
            data.setdefault("type", "misc")
            data.setdefault("rarity", "common")
            data.setdefault("slot", None)
            data.setdefault("damage", 0)
            data.setdefault("defense", 0)
            data.setdefault("value", 0)
            data.setdefault("weight", 1)
            data.setdefault("stackable", False)

            # consumabili
            data.setdefault("effects", {})  # es: {"hp": 20, "mana": 10}

            # =========================
            # REGISTRA
            # =========================
            ITEMS[name] = data

            if vnum is not None:
                ITEMS[str(vnum)] = data

            print(f"[OK] Item caricato: {name}")

        except json.JSONDecodeError as e:
            print(f"[ERRORE JSON] {file}: {e}")

        except Exception as e:
            print(f"[ERRORE] {file}: {e}")

    print(f"[ITEMS] Totale: {len(ITEMS)}")


# =========================
# GET ITEM TEMPLATE
# =========================
def get_item(key):

    if not key:
        return None

    return ITEMS.get(str(key).lower())


# =========================
# CREATE ITEM INSTANCE
# =========================
def create_item(key):

    template = get_item(key)

    if not template:
        return None

    # copia profonda sicura
    item = dict(template)

    # runtime fields
    item["id"] = id(item)  # unico in memoria

    return item


# =========================
# LIST ITEMS (DEBUG / BUILDER)
# =========================
def list_items():
    return list(set([v["name"] for v in ITEMS.values() if isinstance(v, dict)]))