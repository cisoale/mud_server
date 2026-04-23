import random


def calculate_gold(mob):

    base_min = mob.get("gold_min", 0)
    base_max = mob.get("gold_max", 0)

    if base_max <= 0:
        return 0

    level = mob.get("level", 1)

    # scaling leggero (non rompe bilanciamento)
    scale = 1 + (level * 0.1)

    min_gold = int(base_min * scale)
    max_gold = int(base_max * scale)

    return random.randint(min_gold, max_gold)