import os
import json

from config import MOBS_DIR


def get_mobs():

    mobs = []

    print("MOBS_DIR =", MOBS_DIR)

    for root, dirs, files in os.walk(MOBS_DIR):

        for file in files:

            if not file.endswith(".json"):
                continue

            path = os.path.join(root, file)

            print("LOADING:", path)

            try:

                with open(path, "r", encoding="utf-8") as f:

                    data = json.load(f)

                    if not isinstance(data, dict):
                        continue

                    if data.get("vnum") is None:

                        print(
                            "MOB SENZA VNUM:",
                            path
                        )

                        data["vnum"] = 0

                    mobs.append(data)

            except Exception as e:

                print("ERRORE FILE:", path)

                print(e)

    mobs.sort(
        key=lambda m: int(
            m.get("vnum", 0) or 0
        )
    )

    return mobs


def save_mob(mob):

    vnum = mob.get("vnum")

    if vnum is None:
        return False

    path = os.path.join(
        MOBS_DIR,
        f"{vnum}.json"
    )

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            mob,
            f,
            indent=4,
            ensure_ascii=False
        )

    return True