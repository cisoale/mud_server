import sys
import os
import json
from flask import Flask, request, send_from_directory

# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

sys.path.append(PROJECT_ROOT)

app = Flask(__name__)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MOBS_FOLDER = os.path.join(DATA_DIR, "mobs")

os.makedirs(MOBS_FOLDER, exist_ok=True)

print("=== VISUAL BUILDER INIT ===")
print("MOBS:", MOBS_FOLDER)

# =========================
# VNUM
# =========================
def generate_vnum():
    existing = set()

    for file in os.listdir(MOBS_FOLDER):
        if file.endswith(".json"):
            try:
                with open(os.path.join(MOBS_FOLDER, file), encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("vnum"):
                        existing.add(int(data["vnum"]))
            except:
                pass

    v = 1000
    while v in existing:
        v += 1

    return v


# =========================
# STATIC
# =========================
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "editor_visual.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(BASE_DIR, path)


# =========================
# GET MOBS
# =========================
@app.route("/mobs")
def get_mobs():
    mobs = []

    for file in os.listdir(MOBS_FOLDER):
        if file.endswith(".json"):
            try:
                with open(os.path.join(MOBS_FOLDER, file), encoding="utf-8") as f:
                    data = json.load(f)
                    data["_file"] = file
                    mobs.append(data)
            except Exception as e:
                print("[ERRORE LOAD]", file, e)

    return mobs


# =========================
# SAVE MOB
# =========================
@app.route("/save_mob", methods=["POST"])
def save_mob():

    data = request.json

    if not data or not data.get("name"):
        return {"status": "error", "message": "Nome mancante"}

    try:
        # =========================
        # BASE
        # =========================
        mob = {
            "name": data["name"].strip().lower().replace(" ", "_"),
            "description": data.get("description", ""),
            "type": data.get("type", "normal"),

            "level": int(data.get("level", 1)),
            "hp": int(data.get("hp", 10)),
            "damage": int(data.get("damage", 1)),
            "defense": int(data.get("defense", 0)),
            "xp": int(data.get("xp", 10)),

            "gold_min": int(data.get("gold_min", 0)),
            "gold_max": int(data.get("gold_max", 0)),

            "loot": [],
            "death_events": []
        }

        # =========================
        # GOLD FIX
        # =========================
        if mob["gold_min"] > mob["gold_max"]:
            mob["gold_max"] = mob["gold_min"]

        # =========================
        # LOOT FIX
        # =========================
        for l in data.get("loot", []):
            item = l.get("item", "").strip()

            if not item:
                continue

            mob["loot"].append({
                "item": item.lower().replace(" ", "_"),
                "chance": max(0, min(1, float(l.get("chance", 0)))),
                "min": max(1, int(l.get("min", 1))),
                "max": max(1, int(l.get("max", 1)))
            })

        # =========================
        # VNUM
        # =========================
        mob["vnum"] = int(data.get("vnum") or generate_vnum())

        # =========================
        # SAVE
        # =========================
        filename = data.get("_file") or f"{mob['name']}.json"
        path = os.path.join(MOBS_FOLDER, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(mob, f, indent=4, ensure_ascii=False)

        print("[SAVE MOB]", mob["name"])

        return {"status": "ok"}

    except Exception as e:
        print("[ERRORE SAVE]", e)
        return {"status": "error", "message": str(e)}

########
@app.route("/delete_mob", methods=["POST"])
def delete_mob():

    data = request.json
    filename = data.get("_file")

    if not filename:
        return {"status": "error", "message": "File mancante"}

    path = os.path.join(MOBS_FOLDER, filename)

    if not os.path.exists(path):
        return {"status": "error", "message": "File non trovato"}

    try:
        os.remove(path)
        print("[DELETE MOB]", filename)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5001)