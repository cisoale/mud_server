from core.skills import SKILLS


# =========================
# UNLOCK SKILLS
# =========================
def unlock_skills(player, conn=None):
    """
    Sblocca automaticamente le abilità in base a:
    - classe del player
    - livello del player

    Non duplica skill già ottenute.
    """

    if not player:
        return

    pclass = player.get("class")
    level = player.get("level", 1)

    if not pclass:
        return

    # inizializza lista skill
    player.setdefault("skills", [])

    class_skills = SKILLS.get(pclass, {})

    if not class_skills:
        return

    # lista nomi skill già possedute
    owned = {s.get("name") for s in player["skills"] if isinstance(s, dict)}

    for required_level, skills in class_skills.items():

        if level < required_level:
            continue

        for skill in skills:

            name = skill.get("name")

            if not name:
                continue

            # evita duplicati
            if name in owned:
                continue

            # copia sicurezza (no reference bug)
            new_skill = dict(skill)

            player["skills"].append(new_skill)
            owned.add(name)

            # notifica player
            if conn:
                try:
                    conn.send(f"Hai sbloccato: {name}!\n")
                except:
                    pass


# =========================
# GET SKILL
# =========================
def get_skill(player, name):
    """
    Trova una skill per nome (match parziale).
    """

    if not player or not name:
        return None

    name = name.lower()

    for skill in player.get("skills", []):

        skill_name = skill.get("name", "").lower()

        if name in skill_name:
            return skill

    return None


# =========================
# HAS SKILL
# =========================
def has_skill(player, name):
    """
    Controlla se il player possiede una skill.
    """

    return get_skill(player, name) is not None


# =========================
# LIST SKILLS
# =========================
def list_skills(player):
    """
    Ritorna lista nomi skill (debug / UI).
    """

    return [s.get("name") for s in player.get("skills", [])]