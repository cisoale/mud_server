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

# =========================
# INIT
# =========================
app = Flask(__name__)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MOBS_FOLDER = os.path.join(DATA_DIR, "mobs")
ITEMS_FOLDER = os.path.join(DATA_DIR, "items")
ROOMS_FOLDER = os.path.join(DATA_DIR, "rooms")

# crea cartelle se non esistono
os.makedirs(MOBS_FOLDER, exist_ok=True)
os.makedirs(ITEMS_FOLDER, exist_ok=True)
os.makedirs(ROOMS_FOLDER, exist_ok=True)

print("=== SERVER VISUAL INIT ===")
print("PROJECT_ROOT:", PROJECT_ROOT)
print("MOBS:", MOBS_FOLDER)
print("==========================")

# =========================
# IMPORT CORE
# =========================
from core.mob_loader import normalize_mob


# =========================
# GENERATE VNUM
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

    vnum = 1000
    while vnum in existing:
        vnum += 1

    return vnum


# =========================
# STATIC FILES
# =========================
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(BASE_DIR, path)


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "editor_visual.html")


@app.route("/editor_visual")
def editor_visual():
    return send_from_directory(BASE_DIR, "editor_visual.html")


# =========================
# LOAD MOBS
# =========================
@app.route("/mobs")
def get_mobs():
    mobs = []

    for file in os.listdir(MOBS_FOLDER):
        if file.endswith(".json"):
            path = os.path.join(MOBS_FOLDER, file)

            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                    data["_file"] = file
                    mobs.append(data)
            except Exception as e:
                print("[ERRORE MOB]", file, e)

    print(f"[MOBS] {len(mobs)} caricati")
    return mobs


# =========================
# SAVE MOB
# =========================
@app.route("/save_mob", methods=["POST"])
def save_mob():

    data = request.json

    if not data or "name" not in data:
        return {"status": "error", "message": "Nome mancante"}

    # =========================
    # FIX NUMERICI
    # =========================
    int_fields = [
        "level", "hp", "damage",
        "defense", "xp",
        "gold_min", "gold_max"
    ]

    for field in int_fields:
        try:
            data[field] = int(data.get(field, 0))
        except:
            data[field] = 0

    # =========================
    # DEFAULT
    # =========================
    data.setdefault("inventory", [])
    data.setdefault("loot", [])
    data.setdefault("death_events", [])

    # =========================
    # NORMALIZE
    # =========================
    mob = normalize_mob(data)

    # fix gold
    if mob["gold_min"] > mob["gold_max"]:
        mob["gold_max"] = mob["gold_min"]

    # =========================
    # FIX VNUM
    # =========================
    if not mob.get("vnum"):
        mob["vnum"] = generate_vnum()

    mob["vnum"] = int(mob["vnum"])

    # =========================
    # FILE NAME
    # =========================
    safe_name = mob["name"].lower().replace(" ", "_")

    if not safe_name:
        return {"status": "error", "message": "Nome non valido"}

    filename = data.get("_file") or f"{safe_name}.json"
    path = os.path.join(MOBS_FOLDER, filename)

    print("[SAVE PATH]", path)

    # =========================
    # SAVE
    # =========================
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(mob, f, indent=4, ensure_ascii=False)

        print(f"[SAVE MOB] {mob['name']} (vnum: {mob['vnum']})")
        return {"status": "ok"}

    except Exception as e:
        print("[ERRORE SAVE MOB]", e)
        return {"status": "error", "message": str(e)}


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5001)