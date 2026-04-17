import random


def calculate_crit(player):

    base_crit = 5  # base %

    dex = player.get("dex", 10)
    dex_bonus = dex // 2

    weapon = player.get("equipment", {}).get("weapon")

    weapon_crit = 0
    if weapon:
        weapon_crit = weapon.get("crit", 0)

    total_crit = base_crit + dex_bonus + weapon_crit

    roll = random.randint(1, 100)

    return roll <= total_crit


def apply_crit(damage):

    return int(damage * 2)