# =========================
# UTILS
# =========================

def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def safe_str(value, default=""):
    if value is None:
        return default
    return str(value)


def normalize_name(name):
    return safe_str(name).lower().strip().replace(" ", "_")


# =========================
# ITEM NORMALIZER
# =========================

VALID_ITEM_TYPES = ["weapon", "armor", "consumable", "misc"]
VALID_RARITY = ["common", "uncommon", "rare", "epic", "legendary"]
VALID_SLOTS = ["weapon", "head", "chest", "legs", "feet", "hands", "shield"]


def normalize_item(data):

    if not data or not data.get("name"):
        raise ValueError("Item name is required")

    item_type = data.get("type", "misc")

    if item_type not in VALID_ITEM_TYPES:
        item_type = "misc"

    rarity = data.get("rarity", "common")
    if rarity not in VALID_RARITY:
        rarity = "common"

    name = normalize_name(data["name"])

    item = {
        "name": name,
        "display_name": safe_str(data.get("display_name", data["name"])),

        "description": safe_str(data.get("description", "")),

        "type": item_type,
        "rarity": rarity,

        "value": safe_int(data.get("value", 10)),
        "weight": safe_int(data.get("weight", 1)),

        "vnum": safe_int(data.get("vnum", 0)),

        "stackable": bool(data.get("stackable", False)),
        "quantity": safe_int(data.get("quantity", 1)),

        "effects": data.get("effects", {}) or {},
        "flags": data.get("flags", []) or [],

        "requirements": data.get("requirements", {"level": 1}) or {"level": 1}
    }

    # 🔥 SLOT solo per equip
    if item_type in ["weapon", "armor"]:
        slot = data.get("slot")
        if slot in VALID_SLOTS:
            item["slot"] = slot
        else:
            item["slot"] = None

    # 🔥 STATS
    if item_type == "weapon":
        item["damage"] = safe_int(data.get("damage", 1))
    else:
        item["damage"] = 0

    if item_type == "armor":
        item["defense"] = safe_int(data.get("defense", 1))
    else:
        item["defense"] = 0

    # 🔥 CONSUMABLE
    if item_type == "consumable":
        item["consumable"] = data.get("consumable", {"heal": 0})
    else:
        item["consumable"] = None

    return item


# =========================
# MOB NORMALIZER
# =========================

VALID_MOB_TYPES = ["normal", "elite", "boss"]


def normalize_mob(data):

    if not data or not data.get("name"):
        raise ValueError("Mob name is required")

    name = normalize_name(data["name"])

    mob_type = data.get("type", "normal")
    if mob_type not in VALID_MOB_TYPES:
        mob_type = "normal"

    mob = {
        "name": name,
        "display_name": safe_str(data.get("display_name", data["name"])),

        "description": safe_str(data.get("description", "")),

        "type": mob_type,
        "level": safe_int(data.get("level", 1)),

        "hp": safe_int(data.get("hp", 10)),
        "damage": safe_int(data.get("damage", 1)),
        "defense": safe_int(data.get("defense", 0)),

        "xp": safe_int(data.get("xp", 10)),

        "gold_min": safe_int(data.get("gold_min", 0)),
        "gold_max": safe_int(data.get("gold_max", 0)),

        "loot": normalize_loot(data.get("loot", [])),

        "loot_script": data.get("loot_script"),

        "ai": normalize_ai(data.get("ai")),
        "flags": data.get("flags", []) or [],

        "spawn": normalize_spawn(data.get("spawn"))
    }

    return mob


# =========================
# LOOT SYSTEM
# =========================

def normalize_loot(loot_list):

    if not isinstance(loot_list, list):
        return []

    normalized = []

    for l in loot_list:
        if not isinstance(l, dict):
            continue

        item = l.get("item")
        chance = safe_int(l.get("chance", 0))

        if not item:
            continue

        normalized.append({
            "item": normalize_name(item),
            "chance": max(0, min(chance, 100))
        })

    return normalized


# =========================
# AI SYSTEM
# =========================

def normalize_ai(ai):

    if not isinstance(ai, dict):
        return {"aggressive": False}

    return {
        "aggressive": bool(ai.get("aggressive", False)),
        "wander": bool(ai.get("wander", False)),
        "assist": bool(ai.get("assist", False))
    }


# =========================
# SPAWN SYSTEM
# =========================

def normalize_spawn(spawn):

    if not isinstance(spawn, dict):
        return {"respawn_time": 60}

    return {
        "respawn_time": safe_int(spawn.get("respawn_time", 60)),
        "max": safe_int(spawn.get("max", 1))
    }
