from flask import Flask, request, jsonify, send_from_directory
import os
import json

import sys
import os

# 🔥 FIX PATH ROOT
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# =========================
# INIT
# =========================
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOMS_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data/rooms"))
MOBS_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "../data/mobs"))
ITEMS_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "../data/items"))

print("=== SERVER INIT ===")
print("BASE_DIR:", BASE_DIR)
print("MOBS:", MOBS_FOLDER)
print("ITEMS:", ITEMS_FOLDER)
print("===================")

# 🔥 IMPORTANTE
from core.mob_loader import normalize_mob


# =========================
# STATIC FILES
# =========================
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/editor")
def editor_page():
    return send_from_directory(".", "editor.html")


# =========================
# MOBS
# =========================
@app.route("/mobs")
def get_mobs():

    mobs = []

    if not os.path.exists(MOBS_FOLDER):
        print("[ERRORE] Cartella mobs non trovata:", MOBS_FOLDER)
        return []

    for file in os.listdir(MOBS_FOLDER):

        if not file.endswith(".json"):
            continue

        path = os.path.join(MOBS_FOLDER, file)

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

                # utile per editor
                data["_file"] = file

                mobs.append(data)

        except Exception as e:
            print(f"[ERRORE MOB] {file}: {e}")

    print(f"[MOBS] Caricati: {len(mobs)}")

    return mobs


@app.route("/save_mob", methods=["POST"])
def save_mob():

    data = request.json

    if not data or "name" not in data:
        return {"status": "error", "message": "Nome mancante"}

    # =========================
    # FIX NUMERICI
    # =========================
    int_fields = [
        "level", "hp", "damage", "defense",
        "xp", "gold_min", "gold_max"
    ]

    for field in int_fields:
        try:
            data[field] = int(data.get(field, 0))
        except:
            data[field] = 0

    # =========================
    # DEFAULT SICURI
    # =========================
    data.setdefault("inventory", [])
    data.setdefault("loot", [])
    data.setdefault("death_events", [])

    # =========================
    # NORMALIZZAZIONE 🔥
    # =========================
    mob = normalize_mob(data)

    # =========================
    # FIX GOLD RANGE
    # =========================
    if mob["gold_min"] > mob["gold_max"]:
        mob["gold_max"] = mob["gold_min"]

    # =========================
    # FILE NAME
    # =========================
    filename = data.get("_file") or f"{mob['name'].lower().replace(' ', '_')}.json"
    path = os.path.join(MOBS_FOLDER, filename)

    # =========================
    # SAVE
    # =========================
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(mob, f, indent=4, ensure_ascii=False)

        print(f"[SAVE MOB] {mob['name']}")

        return {"status": "ok"}

    except Exception as e:
        print("[ERRORE SAVE MOB]", e)
        return {"status": "error", "message": str(e)}


# =========================
# ITEMS
# =========================
@app.route("/items")
def get_items():

    items = []

    if not os.path.exists(ITEMS_FOLDER):
        print("[ERRORE] Cartella items non trovata:", ITEMS_FOLDER)
        return []

    for file in os.listdir(ITEMS_FOLDER):

        if not file.endswith(".json"):
            continue

        path = os.path.join(ITEMS_FOLDER, file)

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

                data["_file"] = file
                items.append(data)

        except Exception as e:
            print(f"[ERRORE ITEM] {file}: {e}")

    print(f"[ITEMS] Caricati: {len(items)}")

    return items


@app.route("/save_item", methods=["POST"])
def save_item():

    data = request.json

    if not data or "name" not in data:
        return {"status": "error", "message": "Nome mancante"}

    filename = data.get("_file") or f"{data['name'].lower()}.json"
    path = os.path.join(ITEMS_FOLDER, filename)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"[SAVE ITEM] {data['name']}")

        return {"status": "ok"}

    except Exception as e:
        print("[ERRORE SAVE ITEM]", e)
        return {"status": "error", "message": str(e)}


# =========================
# ROOMS
# =========================
@app.route("/rooms")
def get_rooms():

    rooms = []

    if not os.path.exists(ROOMS_DIR):
        return {"rooms": []}

    for file in os.listdir(ROOMS_DIR):

        if file.endswith(".json"):
            path = os.path.join(ROOMS_DIR, file)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    room = json.load(f)
                    rooms.append(room)

            except Exception as e:
                print("[ERRORE ROOM]", file, e)

    return {"rooms": rooms}


@app.route("/save_rooms", methods=["POST"])
def save_rooms():

    data = request.json
    rooms = data.get("rooms", [])

    os.makedirs(ROOMS_DIR, exist_ok=True)

    try:
        for room in rooms:

            vnum = room.get("vnum")

            if not vnum:
                print("[SKIP] Room senza vnum")
                continue

            path = os.path.join(ROOMS_DIR, f"{vnum}.json")

            with open(path, "w", encoding="utf-8") as f:
                json.dump(room, f, indent=4, ensure_ascii=False)

            print(f"[SAVE] Room {vnum}")

        return {"status": "ok"}

    except Exception as e:
        print("[ERRORE SAVE ROOM]", e)
        return {"status": "error", "message": str(e)}


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)