from core.skill_system import unlock_skills


# =========================
# XP PER LIVELLO
# =========================
def xp_to_next_level(level):
    """
    Calcola l'XP necessaria per il prossimo livello.
    Formula semplice ma scalabile.
    """
    return level * 100


# =========================
# LEVEL UP CHECK
# =========================
def check_level_up(player, conn=None):
    """
    Controlla se il player sale di livello.
    - Gestisce più level-up consecutivi
    - Aggiorna stats
    - Sblocca skill
    """

    if not player:
        return False

    # sicurezza dati
    player.setdefault("level", 1)
    player.setdefault("xp", 0)
    player.setdefault("hp", 100)
    player.setdefault("damage", 2)
    player.setdefault("defense", 0)

    leveled_up = False

    # loop per multi-level up
    while player["xp"] >= xp_to_next_level(player["level"]):

        required_xp = xp_to_next_level(player["level"])

        player["xp"] -= required_xp
        player["level"] += 1

        # =========================
        # INCREMENTO STATS
        # =========================
        player["hp"] += 10
        player["damage"] += 1
        player["defense"] += 1

        leveled_up = True

        # =========================
        # MESSAGGIO
        # =========================
        if conn:
            try:
                conn.send(f"\n✨ SEI SALITO AL LIVELLO {player['level']}! ✨\n")
            except:
                pass

        # =========================
        # SBLOCCO SKILL (FIX)
        # =========================
        unlock_skills(player, conn)

    return leveled_up