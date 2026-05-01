import os
import json
from config import ROOMS_DIR


# =========================
# UTILS
# =========================

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================
# LOAD ROOMS (ROBUSTO)
# =========================

def get_rooms():
    ensure_dir(ROOMS_DIR)

    print("📂 ROOMS DIR:", ROOMS_DIR)

    rooms = []
    index = {}

    for filename in os.listdir(ROOMS_DIR):
        if not filename.endswith(".json"):
            continue

        path = os.path.join(ROOMS_DIR, filename)

        try:
            data = load_json(path)

            # 🔥 supporto formato {"room": {...}}
            if isinstance(data, dict) and "room" in data:
                data = data["room"]

            # 🔥 FIX VNUM
            vnum = data.get("vnum")

            # fallback da nome file
            if vnum is None or vnum == "":
                try:
                    vnum = int(filename.replace(".json", ""))
                except:
                    print("❌ FILE SENZA VNUM VALIDO:", filename)
                    continue

            # forza int
            try:
                vnum = int(vnum)
            except:
                print("❌ VNUM NON NUMERICO:", filename, vnum)
                continue

            data["vnum"] = vnum
            data["_file"] = filename

            rooms.append(data)
            index[vnum] = data

        except Exception as e:
            print("❌ ERRORE ROOM:", filename, e)

    print(f"✅ ROOMS CARICATE: {len(rooms)}")

    return {
        "rooms": rooms,
        "index": index
    }


# =========================
# SAVE ROOM (MERGE SICURO)
# =========================

def save_room(new_room):
    ensure_dir(ROOMS_DIR)

    vnum = new_room.get("vnum")

    if vnum is None:
        raise ValueError("Room senza VNUM")

    try:
        vnum = int(vnum)
    except:
        raise ValueError("VNUM non valido")

    path = os.path.join(ROOMS_DIR, f"{vnum}.json")

    # carica vecchio file
    if os.path.exists(path):
        try:
            old_room = load_json(path)
        except:
            old_room = {}
    else:
        old_room = {}

    # supporto nested
    if isinstance(old_room, dict) and "room" in old_room:
        old_room = old_room["room"]

    # =========================
    # MERGE
    # =========================

    merged = old_room.copy()

    for key, value in new_room.items():

        if key.startswith("_"):
            continue

        # salva posizione mappa
        if key == "pos":
            merged["pos"] = value
            continue

        # exits
        if key == "exits":
            merged["exits"] = value or {}
            continue

        merged[key] = value

    merged["vnum"] = vnum

    save_json(path, merged)

    print(f"💾 ROOM SALVATA: {vnum}")

    return merged


# =========================
# DELETE ROOM
# =========================

def delete_room(vnum):
    try:
        vnum = int(vnum)
    except:
        return False

    path = os.path.join(ROOMS_DIR, f"{vnum}.json")

    if os.path.exists(path):
        os.remove(path)
        print(f"🗑 ROOM ELIMINATA: {vnum}")
        return True

    return False