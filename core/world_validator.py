import json


def validate_and_fix_room(data):

    changed = False

    # =========================
    # CAMPI BASE
    # =========================
    if "name" not in data:
        data["name"] = "Stanza senza nome"
        changed = True

    if "description" not in data:
        data["description"] = ""
        changed = True

    if "items" not in data:
        data["items"] = []
        changed = True

    if "mobs" not in data:
        data["mobs"] = []
        changed = True

    # =========================
    # COORDINATE
    # =========================
    if "x" not in data:
        data["x"] = 100
        changed = True

    if "y" not in data:
        data["y"] = 100
        changed = True

    # fix pos vecchio formato
    if "pos" in data:
        data["x"] = data["pos"].get("x", data["x"])
        data["y"] = data["pos"].get("y", data["y"])
        del data["pos"]
        changed = True

    # =========================
    # EXITS
    # =========================
    if "exits" not in data:
        data["exits"] = {}
        changed = True

    for direction in list(data["exits"].keys()):

        exit_data = data["exits"][direction]

        # 🔥 FIX FORMATO NUMERO
        if isinstance(exit_data, int):
            data["exits"][direction] = {
                "to": exit_data,
                "closed": False,
                "locked": False,
                "secret": False
            }
            changed = True
            continue

        # 🔥 FIX STRUTTURA
        if "to" not in exit_data:
            print(f"[WARNING] exit senza 'to' rimossa ({direction})")
            del data["exits"][direction]
            changed = True
            continue

        # default flags
        exit_data.setdefault("closed", False)
        exit_data.setdefault("locked", False)
        exit_data.setdefault("secret", False)

    return data, changed