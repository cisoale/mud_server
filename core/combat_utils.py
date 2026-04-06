def create_corpse(mob):
    corpse = {
        "name": f"corpo di {mob['name']}",
        "type": "corpse",
        "inventory": mob.get("inventory", [])
    }

    return corpse