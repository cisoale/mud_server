def create_corpse(mob):
    corpse = {
        "name": f"corpo di {mob['name']}",
        "type": "corpse",
        "inventory": mob.get("inventory", [])
    }

    return corpse

def get_total_damage(player):
    base = 2

    weapon = player["equipment"].get("weapon")

    if weapon:
        base += weapon.get("damage", 0)

    return base


def get_total_armor(player):
    armor = 0

    for item in player["equipment"].values():
        if item:
            armor += item.get("armor", 0)

    return armor