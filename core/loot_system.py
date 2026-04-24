import random
import os
import json

ITEMS_PATH = "data/items"


def get_item_data(name):
    path = os.path.join(ITEMS_PATH, f"{name}.json")

    if not os.path.exists(path):
        return {}

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def rarity_color(name, rarity):
    colors = {
        "common": "",
        "uncommon": "[Verde] ",
        "rare": "[Blu] ",
        "epic": "[Viola] ",
        "legendary": "[Oro] "
    }
    return f"{colors.get(rarity, '')}{name}"


def generate_loot_json(mob):

    loot = []

    for entry in mob.get("loot", []):

        chance = entry.get("chance", 0)
        rarity = entry.get("rarity", "common")

        if rarity == "rare":
            chance *= 0.8
        elif rarity == "epic":
            chance *= 0.5
        elif rarity == "legendary":
            chance *= 0.2

        if random.random() <= chance:

            qty = random.randint(
                entry.get("min", 1),
                entry.get("max", 1)
            )

            loot.append({
                "name": entry.get("item"),
                "quantity": qty
            })

    return loot