def execute(player, args, cmd=None):
    return (
        f"Livello: {player.get('level')}\n"
        f"XP: {player.get('xp')}/{player.get('xp_to_next')}\n"
        f"HP: {player.get('hp')}/{player.get('max_hp')}"
    )