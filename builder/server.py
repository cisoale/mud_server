from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)


# =========================
# 📁 PATH
# =========================
ROOMS_PATH = "../data/rooms"
MOBS_PATH = "../data/mobs.json"
ITEMS_PATH = "../data/items.json"


# =========================
# 🏠 HOME
# =========================
@app.route("/")
def index():
    return render_template("index.html")


# =========================
# 🗺️ LOAD ROOMS
# =========================
@app.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = []

    if not os.path.exists(ROOMS_PATH):
        os.makedirs(ROOMS_PATH)

    for file in os.listdir(ROOMS_PATH):
        if file.endswith(".json"):
            with open(os.path.join(ROOMS_PATH, file)) as f:
                rooms.append(json.load(f))

    return jsonify(rooms)


# =========================
# 💾 SAVE ROOM
# =========================
@app.route("/save_room", methods=["POST"])
def save_room():
    data = request.json

    if not os.path.exists(ROOMS_PATH):
        os.makedirs(ROOMS_PATH)

    vnum = data.get("vnum")
    path = os.path.join(ROOMS_PATH, f"{vnum}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    return {"status": "ok"}


# =========================
# 👹 LOAD MOBS
# =========================
@app.route("/mobs", methods=["GET"])
def get_mobs():
    if not os.path.exists(MOBS_PATH):
        with open(MOBS_PATH, "w") as f:
            json.dump([], f)

    with open(MOBS_PATH) as f:
        return jsonify(json.load(f))


# =========================
# 💾 SAVE MOB
# =========================
@app.route("/save_mob", methods=["POST"])
def save_mob():
    data = request.json

    if not os.path.exists(MOBS_PATH):
        with open(MOBS_PATH, "w") as f:
            json.dump([], f)

    with open(MOBS_PATH) as f:
        mobs = json.load(f)

    existing = next((m for m in mobs if m["name"] == data["name"]), None)

    if existing:
        existing.update(data)
    else:
        mobs.append(data)

    with open(MOBS_PATH, "w") as f:
        json.dump(mobs, f, indent=4)

    return {"status": "ok"}


# =========================
# 🎒 LOAD ITEMS
# =========================
@app.route("/items", methods=["GET"])
def get_items():
    if not os.path.exists(ITEMS_PATH):
        with open(ITEMS_PATH, "w") as f:
            json.dump([], f)

    with open(ITEMS_PATH) as f:
        return jsonify(json.load(f))


# =========================
# 💾 SAVE ITEM
# =========================
@app.route("/save_item", methods=["POST"])
def save_item():
    data = request.json

    if not os.path.exists(ITEMS_PATH):
        with open(ITEMS_PATH, "w") as f:
            json.dump([], f)

    with open(ITEMS_PATH) as f:
        items = json.load(f)

    existing = next((i for i in items if i["name"] == data["name"]), None)

    if existing:
        existing.update(data)
    else:
        items.append(data)

    with open(ITEMS_PATH, "w") as f:
        json.dump(items, f, indent=4)

    return {"status": "ok"}


# =========================
# 🚀 START
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)