from flask import Flask, request, jsonify, send_from_directory
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")
JS_DIR = os.path.join(UI_DIR, "js")

ROOMS_DIR = r"C:\Users\Ale\Desktop\Realm of Lord\mud_server\data\rooms"

app = Flask(__name__)


# ================= STATIC =================

@app.route("/")
def index():
    return send_from_directory(UI_DIR, "rooms.html")

@app.route("/js/<path:filename>")
def js_files(filename):
    return send_from_directory(JS_DIR, filename)


# ================= UTILS =================

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ================= API =================

@app.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = []

    for file in os.listdir(ROOMS_DIR):
        if not file.endswith(".json"):
            continue

        path = os.path.join(ROOMS_DIR, file)

        try:
            data = load_json(path)

            if "vnum" not in data:
                data["vnum"] = int(file.replace(".json", ""))

            rooms.append(data)

        except Exception as e:
            print("ERROR:", file, e)

    return jsonify({"rooms": rooms})


@app.route("/rooms", methods=["POST"])
def save_room():
    data = request.json

    vnum = data.get("vnum")
    if not vnum:
        return {"error": "no vnum"}, 400

    path = os.path.join(ROOMS_DIR, f"{vnum}.json")

    if os.path.exists(path):
        try:
            old = load_json(path)
        except:
            old = {}
    else:
        old = {}

    merged = {**old, **data}

    save_json(path, merged)

    return {"ok": True}


# ================= START =================

if __name__ == "__main__":
    print("=== MAP BUILDER PRO ===")
    app.run(debug=True, port=5005)