def xp_to_next_level(level):
    """
    Formula crescita XP (scalabile)
    """
    return level * 100


def check_level_up(player, conn=None):

    player.setdefault("level", 1)
    player.setdefault("xp", 0)

    leveled_up = False

    while player["xp"] >= xp_to_next_level(player["level"]):

        player["xp"] -= xp_to_next_level(player["level"])
        player["level"] += 1

        # incremento stats
        player["hp"] = player.get("hp", 100) + 10
        player["damage"] = player.get("damage", 2) + 1
        player["defense"] = player.get("defense", 0) + 1

        leveled_up = True

        if conn:
            conn.send(f"\n✨ SEI SALITO AL LIVELLO {player['level']}! ✨\n")

    return leveled_up