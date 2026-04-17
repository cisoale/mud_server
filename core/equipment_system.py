def get_weapon_damage(player):

    weapon = player.get("equipment", {}).get("weapon")

    if not weapon:
        return 0

    return weapon.get("damage", 0)


def get_total_armor(player):

    equipment = player.get("equipment", {})

    total = 0

    for item in equipment.values():

        if isinstance(item, dict):
            total += item.get("armor", 0)

    return total