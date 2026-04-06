def init_player_state(player):
    player.setdefault("inventory", [])

    player.setdefault("equipment", {
        "head": None,
        "chest": None,
        "legs": None,
        "feet": None,
        "hands": None,
        "weapon": None,
        "shield": None,
        "ring": None,
        "amulet": None
    })

    return player