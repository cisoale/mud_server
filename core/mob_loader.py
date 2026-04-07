import os
import json

mobs_data = {}


def load_mobs():
    folder = "data/mobs"

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

            name = data["name"]
            mobs_data[name] = data

    print(f"[MOBS] Caricati: {list(mobs_data.keys())}")