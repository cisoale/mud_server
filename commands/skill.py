from core.world import get_room
from core.skill_system import get_skill
from core.skill_combat import apply_skill
from core.death_system import handle_death  # 🔥 NUOVO


# =========================
# TROVA TARGET
# =========================
def find_target(room, name):

    name = name.lower()

    for mob in room.mobs:
        if name in mob.get("name", "").lower():
            return mob

    for p in room.players:
        if name in p.get("name", "").lower():
            return p

    return None


# =========================
# BROADCAST
# =========================
def broadcast(room, message):

    for p in room.players:
        conn = p.get("conn")
        if conn:
            conn.send(message)


# =========================
# COMANDO SKILL
# =========================
def execute(player, conn, args):

    if len(args) < 2:
        conn.send("Uso: skill <abilità> <target>\n")
        return

    skill_name = args[0]
    target_name = " ".join(args[1:])

    # =========================
    # TROVA SKILL
    # =========================
    skill = get_skill(player, skill_name)

    if not skill:
        conn.send("Non conosci questa abilità.\n")
        return

    # =========================
    # TROVA TARGET
    # =========================
    room = get_room(player.get("room"))
    target = find_target(room, target_name)

    if not target:
        conn.send("Target non trovato.\n")
        return

    # =========================
    # APPLICA SKILL
    # =========================
    damage = apply_skill(player, target, skill)

    msg = f"{player['name']} usa {skill['name']} su {target['name']} ({damage} danni)\n"
    broadcast(room, msg)

    # =========================
    # MORTE (CENTRALIZZATA)
    # =========================
    if target.get("hp", 0) <= 0:

        death_msg = f"{target['name']} è stato sconfitto!\n"
        broadcast(room, death_msg)

        # 🔥 TUTTO GESTITO QUI
        handle_death(player, target, room, broadcast)