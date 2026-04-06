import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def load_json(relative_path):
    path = os.path.join(BASE_DIR, relative_path)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


races = load_json("data/races.json")
classes = load_json("data/classes.json")

print("RACES:", races)