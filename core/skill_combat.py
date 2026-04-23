from core.stats import get_total_stats, get_weapon_damage


def apply_skill(player, target, skill):

    stats = get_total_stats(player)

    base_damage = skill.get("damage", 0)

    # scaling
    damage = base_damage + stats.get("str", 0) + get_weapon_damage(player)

    # riduzione difesa target
    defense = target.get("defense", 0)
    final_damage = max(1, damage - defense)

    target["hp"] -= final_damage

    return final_damage