from core.set_bonus import get_set_bonus
from core.effects import get_item_effects


def get_total_stats(player):

    total = dict(player.get("stats", {}))

    # bonus equip
    for item in player.get("equipment", {}).values():
        for stat, value in item.get("stats", {}).items():
            total[stat] = total.get(stat, 0) + value

    # 🔥 SET BONUS
    set_bonus = get_set_bonus(player)

    for stat, value in set_bonus.items():
        total[stat] = total.get(stat, 0) + value

    return total

def get_total_stats(player):

    total = dict(player.get("stats", {}))

    for item in player.get("equipment", {}).values():

        if not item:
            continue

        for stat, value in item.get("stats", {}).items():
            total[stat] = total.get(stat, 0) + value

    return total

def get_weapon_damage(player):

    weapon = player.get("equipment", {}).get("weapon")

    if not weapon:
        return 1

    return weapon.get("damage", 1)


def get_total_defense(player):

    defense = 0

    for item in player.get("equipment", {}).values():
        defense += item.get("defense", 0)

    return defense