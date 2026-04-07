from flask import Flask, request, jsonify, render_template
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data")
import json

app = Flask(__name__)

DATA_PATH = "../data"


# 🏠 HOME
@app.route("/")
def index():
    return render_template("index.html")


# 💾 SALVA ROOM
@app.route("/save_room", methods=["POST"])
def save_room():
    data = request.json

    folder = os.path.join(DATA_PATH, "rooms")
    os.makedirs(folder, exist_ok=True)

    vnum = data.get("vnum")
    path = os.path.join(folder, f"{vnum}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[BUILDER] Room salvata: {path}")

    return jsonify({"status": "ok"})

    folder = os.path.join(DATA_PATH, "rooms")

    # 🔥 CREA CARTELLA SE NON ESISTE
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, f"{vnum}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[BUILDER] Room salvata: {path}")

    return jsonify({"status": "ok"})
# 👹 SALVA MOB
@app.route("/save_mob", methods=["POST"])
def save_mob():
    data = request.json
    name = data["name"]

    path = os.path.join(DATA_PATH, "mobs", f"{name}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({"status": "ok"})


# 🎒 SALVA ITEM
@app.route("/save_item", methods=["POST"])
def save_item():
    data = request.json
    name = data["name"]

    path = os.path.join(DATA_PATH, "items", f"{name}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return jsonify({"status": "ok"})

@app.route("/rooms")
def get_rooms():
    folder = os.path.join(DATA_PATH, "rooms")
    rooms = []

    for file in os.listdir(folder):
        with open(os.path.join(folder, file)) as f:
            data = json.load(f)
            rooms.append(data)

    return jsonify(rooms)

if __name__ == "__main__":
    app.run(port=5000, debug=True)