from core.xp_system import xp_to_next_level


def execute(player, conn, args):

    level = player.get("level", 1)
    xp = player.get("xp", 0)
    hp = player.get("hp", 100)
    dmg = player.get("damage", 2)
    defense = player.get("defense", 0)

    next_xp = xp_to_next_level(level)

    conn.send("\n=== STATS ===\n")
    conn.send(f"Nome: {player.get('name')}\n")
    conn.send(f"Livello: {level}\n")
    conn.send(f"XP: {xp} / {next_xp}\n")
    conn.send(f"HP: {hp}\n")
    conn.send(f"Danno: {dmg}\n")
    conn.send(f"Difesa: {defense}\n")