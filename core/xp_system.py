# =========================
# XP NECESSARIA PER LIVELLO
# =========================
def get_xp_to_next_level(level):
    """
    Formula base scalabile
    """
    return level * 100


# =========================
# AGGIUNTA XP
# =========================
def add_xp(player, amount, conn):

    if amount <= 0:
        return

    # inizializza se mancante
    player.setdefault("xp", 0)
    player.setdefault("level", 1)
    player.setdefault("max_hp", 100)
    player.setdefault("hp", player["max_hp"])
    player.setdefault("str", 10)
    player.setdefault("dex", 10)
    player.setdefault("int", 10)

    player["xp"] += amount

    conn.send(f"Hai guadagnato {amount} XP.\n")

    # =========================
    # LEVEL UP LOOP
    # =========================
    leveled = False

    while player["xp"] >= get_xp_to_next_level(player["level"]):

        needed = get_xp_to_next_level(player["level"])
        player["xp"] -= needed

        player["level"] += 1
        leveled = True

        # =========================
        # BONUS LEVEL UP
        # =========================
        player["max_hp"] += 10
        player["hp"] = player["max_hp"]

        player["str"] += 1
        player["dex"] += 1
        player["int"] += 1

        conn.send(f"\n🔥 LEVEL UP! Sei ora livello {player['level']}!\n")

        conn.send("Le tue statistiche aumentano!\n")
        conn.send("+10 HP\n+1 STR\n+1 DEX\n+1 INT\n")

    # =========================
    # INFO PROGRESSIONE
    # =========================
    current = player["xp"]
    needed = get_xp_to_next_level(player["level"])

    conn.send(f"XP: {current}/{needed}\n")

    return leveled