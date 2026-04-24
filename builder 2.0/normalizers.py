def normalize_item(data):

    item_type = data.get("type", "misc")

    return {
        "name": data["name"].lower().replace(" ", "_"),
        "display_name": data.get("display_name", data["name"]),
        "description": data.get("description", ""),

        "type": item_type,
        "rarity": data.get("rarity", "common"),

        "value": int(data.get("value", 10)),
        "weight": int(data.get("weight", 1)),
        "vnum": int(data.get("vnum", 0)),

        "stackable": False,
        "quantity": 1,

        "slot": data.get("slot") if item_type in ["weapon", "armor"] else None,

        "damage": int(data.get("damage", 0)),
        "defense": int(data.get("defense", 0)),

        "consumable": data.get("consumable") if item_type == "consumable" else None,

        "effects": data.get("effects", {}),
        "flags": data.get("flags", []),

        "requirements": data.get("requirements", {"level": 1})
    }


def normalize_mob(data):

    return {
        "name": data["name"].lower().replace(" ", "_"),
        "display_name": data.get("display_name", data["name"]),
        "description": data.get("description", ""),

        "type": data.get("type", "normal"),
        "level": int(data.get("level", 1)),

        "hp": int(data.get("hp", 10)),
        "damage": int(data.get("damage", 1)),
        "defense": int(data.get("defense", 0)),

        "xp": int(data.get("xp", 10)),

        "gold_min": int(data.get("gold_min", 0)),
        "gold_max": int(data.get("gold_max", 0)),

        "loot": data.get("loot", []),

        "loot_script": data.get("loot_script"),

        "ai": data.get("ai", {"aggressive": False}),
        "flags": data.get("flags", []),

        "spawn": data.get("spawn", {"respawn_time": 60})
    }