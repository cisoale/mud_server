from flask import Flask, request, send_from_directory
import os, json

from config import MOBS_DIR, ITEMS_DIR, ROOMS_DIR
from normalizers import normalize_item, normalize_mob

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")

# =========================
# UTILS
# =========================
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================
# STATIC
# =========================
@app.route("/")
def index():
    return send_from_directory(UI_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(UI_DIR, path)

# =========================
# ITEMS
# =========================
@app.route("/items")
def get_items():
    res = []
    for f in os.listdir(ITEMS_DIR):
        if f.endswith(".json"):
            path = os.path.join(ITEMS_DIR, f)
            res.append(load_json(path))
    return res


@app.route("/save_item", methods=["POST"])
def save_item():
    data = request.json

    if not data.get("name"):
        return {"status": "error", "message": "Nome mancante"}

    item = normalize_item(data)

    path = os.path.join(ITEMS_DIR, f"{item['name']}.json")
    save_json(path, item)

    print("[SAVE ITEM]", path)
    return {"status": "ok"}


@app.route("/delete_item", methods=["POST"])
def delete_item():
    name = request.json.get("name")

    path = os.path.join(ITEMS_DIR, f"{name}.json")

    if os.path.exists(path):
        os.remove(path)
        return {"status": "ok"}

    return {"status": "error"}


# =========================
# MOBS
# =========================
@app.route("/mobs")
def get_mobs():
    res = []
    for f in os.listdir(MOBS_DIR):
        if f.endswith(".json"):
            path = os.path.join(MOBS_DIR, f)
            d = load_json(path)
            d["_file"] = f
            res.append(d)
    return res


@app.route("/save_mob", methods=["POST"])
def save_mob():
    data = request.json

    if not data.get("name"):
        return {"status": "error"}

    mob = normalize_mob(data)

    filename = data.get("_file") or f"{mob['name']}.json"
    path = os.path.join(MOBS_DIR, filename)

    save_json(path, mob)

    print("[SAVE MOB]", path)
    return {"status": "ok"}


@app.route("/delete_mob", methods=["POST"])
def delete_mob():
    f = request.json.get("_file")

    path = os.path.join(MOBS_DIR, f)

    if os.path.exists(path):
        os.remove(path)
        return {"status": "ok"}

    return {"status": "error"}


# =========================
# ROOMS (🔥 NUOVO BLOCCO)
# =========================
@app.route("/rooms")
def get_rooms():

    res = []

    if not os.path.exists(ROOMS_DIR):
        os.makedirs(ROOMS_DIR)

    for f in os.listdir(ROOMS_DIR):
        if f.endswith(".json"):

            path = os.path.join(ROOMS_DIR, f)

            try:
                room = load_json(path)
                res.append(room)
            except Exception as e:
                print("ERRORE ROOM:", f, e)

    print("[LOAD ROOMS]", len(res))

    return {"rooms": res}


@app.route("/save_rooms", methods=["POST"])
def save_rooms():

    data = request.json
    rooms = data.get("rooms", [])

    if not os.path.exists(ROOMS_DIR):
        os.makedirs(ROOMS_DIR)

    print("[SAVE ROOMS]", len(rooms))

    for r in rooms:

        vnum = r.get("vnum")

        if not vnum:
            continue

        filename = f"{vnum}.json"
        path = os.path.join(ROOMS_DIR, filename)

        save_json(path, r)

        print("SALVATA ROOM:", path)

    return {"status": "ok"}


@app.route("/delete_room", methods=["POST"])
def delete_room():

    vnum = request.json.get("vnum")

    path = os.path.join(ROOMS_DIR, f"{vnum}.json")

    if os.path.exists(path):
        os.remove(path)
        return {"status": "ok"}

    return {"status": "error"}


# =========================
# RUN
# =========================
if __name__ == "__main__":
    print("=== BUILDER SERVER ===")
    print("MOBS:", MOBS_DIR)
    print("ITEMS:", ITEMS_DIR)
    print("ROOMS:", ROOMS_DIR)

    app.run(debug=True, port=5005)