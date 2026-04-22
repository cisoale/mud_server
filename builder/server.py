from flask import Flask, request, jsonify
import os
import json
from flask import send_from_directory


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOMS_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data/rooms"))
MOBS_FOLDER = os.path.join(BASE_DIR, "../data/mobs")
ITEMS_FOLDER = os.path.join(BASE_DIR, "../data/items")
print("SERVER FILE:", __file__)
print("=== DEBUG PATH ===")
print("BASE_DIR:", BASE_DIR)
print("MOBS PATH:", MOBS_FOLDER)
print("ITEMS PATH:", ITEMS_FOLDER)
print("==================")
if os.path.exists(MOBS_FOLDER):
    print("FILES:", os.listdir(MOBS_FOLDER))

from flask import request

WORLD_FILE = os.path.join(BASE_DIR, "data", "world.json")

from flask import send_from_directory
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)
@app.route("/")
def index():
    return send_from_directory(".", "index.html")
@app.route("/editor.html")
def editor():
    return send_from_directory(".", "editor.html")

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

                # 🔥 aggiungiamo nome file (utile)
                data["_file"] = file

                mobs.append(data)

        except Exception as e:
            print(f"[ERRORE MOB] {file}: {e}")

    print(f"[MOBS] Caricati: {len(mobs)}")

    return mobs


@app.route("/editor")
def editor_page():
    return send_from_directory(".", "editor.html")


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


@app.route("/save_mob", methods=["POST"])
def save_mob():

    data = request.json

    filename = data.get("_file") or f"{data['name'].lower()}.json"
    path = os.path.join(MOBS_FOLDER, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return {"status": "ok"}


@app.route("/save_item", methods=["POST"])
def save_item():

    data = request.json

    filename = data.get("_file") or f"{data['name'].lower()}.json"
    path = os.path.join(ITEMS_FOLDER, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return {"status": "ok"}
# =========================
# GET ROOMS
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

# =========================
# SAVE ROOM
# =========================
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
        print("[ERRORE SAVE]", e)
        return {"status": "error"}
# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)