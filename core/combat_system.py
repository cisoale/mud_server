import asyncio
import random
from core.world import get_room
from core.save_system import save_player


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

    # 🔥 evita doppio combat
    if player.get("target") or mob.get("target"):
        return

    # init hp
    player.setdefault("current_hp", player.get("hp", 100))
    mob.setdefault("current_hp", mob.get("hp", 20))

    player["target"] = mob
    mob["target"] = player

    conn.send(f"Inizia il combattimento con {mob['name']}!\n")
    broadcast_room(room, f"{player['name']} attacca {mob['name']}!\n", exclude=player)

    # avvia loop async
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

        # se uno dei due sparisce
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
        dmg = calculate_damage(mob, player)
        player["current_hp"] -= dmg

        broadcast_room(room, f"{mob['name']} colpisce {player['name']} per {dmg} danni!\n")

        if player["current_hp"] <= 0:
            handle_player_death(player, room)
            return


# =========================
# DAMAGE SYSTEM
# =========================
def calculate_damage(attacker, defender):

    base = attacker.get("damage", 2)

    # arma equipaggiata
    weapon = attacker.get("equipment", {}).get("weapon")
    if weapon:
        base += weapon.get("damage", 0)

    # difesa
    defense = defender.get("defense", 0)

    dmg = max(1, base - defense)

    # crit
    if random.random() < 0.1:
        dmg *= 2

    return dmg


# =========================
# MOB MORTE
# =========================
def handle_mob_death(player, mob, room):

    broadcast_room(room, f"{mob['name']} muore!\n")

    # XP
    xp = mob.get("xp", 10)
    from core.xp_system import check_level_up

    player["xp"] = player.get("xp", 0) + xp

    player["conn"].send(f"Hai guadagnato {xp} XP!\n")

    check_level_up(player, player["conn"])

    # corpse
    corpse = {
        "name": f"corpo di {mob['name']}",
        "inventory": mob.get("inventory", []),
        "type": "corpse"
    }

    room.items.append(corpse)

    # rimuovi mob
    if mob in room.mobs:
        room.mobs.remove(mob)

    # reset combat
    player["target"] = None
    mob["target"] = None

    save_player(player)


# =========================
# PLAYER MORTE
# =========================
def handle_player_death(player, room):

    broadcast_room(room, f"{player['name']} è morto!\n")

    player["current_hp"] = player.get("hp", 100)

    # respawn
    player["room"] = 1001

    player["target"] = None

    conn = player.get("conn")
    if conn:
        conn.send("Sei morto! Torni al punto di partenza.\n")

    save_player(player)