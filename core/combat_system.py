import asyncio
import random
from core.world import get_room
from core.save_system import save_player
from core.death_system import handle_death  # 🔥 NUOVO


# =========================
# BROADCAST ROOM
# =========================
def broadcast_room(room, message, exclude=None):
    for p in room.players:
        if exclude and p == exclude:
            continue
        conn = p.get("conn")
        if conn:
            conn.send(message)


# =========================
# START COMBAT
# =========================
def start_combat(player, mob, conn):

    room = get_room(player["room"])

    if not room:
        print("[ERRORE COMBAT] room non trovata")
        return

    # evita doppio combat
    if player.get("target") or mob.get("target"):
        return

    # init hp
    player.setdefault("current_hp", player.get("hp", 100))
    mob.setdefault("current_hp", mob.get("hp", 20))

    player["target"] = mob
    mob["target"] = player

    conn.send(f"Inizia il combattimento con {mob['name']}!\n")
    broadcast_room(room, f"{player['name']} attacca {mob['name']}!\n", exclude=player)

    asyncio.create_task(combat_loop(player, mob))


# =========================
# COMBAT LOOP
# =========================
async def combat_loop(player, mob):

    while True:

        await asyncio.sleep(2)

        room = get_room(player["room"])
        if not room:
            return

        if mob not in room.mobs or player not in room.players:
            return

        # =====================
        # PLAYER ATTACK
        # =====================
        dmg = calculate_damage(player, mob)
        mob["current_hp"] -= dmg

        broadcast_room(room, f"{player['name']} colpisce {mob['name']} per {dmg} danni!\n")

        if mob["current_hp"] <= 0:
            handle_mob_death(player, mob, room)
            return

        # =====================
        # MOB ATTACK
        # =====================
        # =====================
        # =====================
# MOB ATTACK
# =====================
        from core.combat_boss import boss_action

        msg = boss_action(mob, player)

        if msg:
          broadcast_room(room, msg + "\n")
        else:
           dmg = calculate_damage(mob, player)
           player["current_hp"] -= dmg

           broadcast_room(room, f"{mob['name']} colpisce {player['name']} per {dmg} danni!\n")


# =========================
# DAMAGE SYSTEM
# =========================
def calculate_damage(attacker, defender):

    base = attacker.get("damage", 2)

    weapon = attacker.get("equipment", {}).get("weapon")
    if weapon:
        base += weapon.get("damage", 0)

    defense = defender.get("defense", 0)

    dmg = max(1, base - defense)

    # crit
    if random.random() < 0.1:
        dmg *= 2

    return dmg


# =========================
# MOB MORTE (REFINED)
# =========================
def handle_mob_death(player, mob, room):

    broadcast_room(room, f"{mob['name']} muore!\n")

    # =========================
    # XP SYSTEM
    # =========================
    xp = mob.get("xp", 10)

    from core.xp_system import check_level_up

    player["xp"] = player.get("xp", 0) + xp

    if player.get("conn"):
        player["conn"].send(f"Hai guadagnato {xp} XP!\n")

    check_level_up(player, player.get("conn"))

    # =========================
    # 🔥 DEATH SYSTEM (GOLD + CORPSE)
    # =========================
    handle_death(player, mob, room, broadcast_room)

    # =========================
    # RESET COMBAT
    # =========================
    player["target"] = None
    mob["target"] = None

    save_player(player)


# =========================
# PLAYER MORTE
# =========================
def handle_player_death(player, room):

    broadcast_room(room, f"{player['name']} è morto!\n")

    player["current_hp"] = player.get("hp", 100)

    player["room"] = 1001
    player["target"] = None

    conn = player.get("conn")
    if conn:
        conn.send("Sei morto! Torni al punto di partenza.\n")

    save_player(player)