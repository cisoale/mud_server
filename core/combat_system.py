import random
from core.world import rooms, broadcast_room


# =========================
# START COMBAT
# =========================
def start_combat(player, mob, conn):

    # evita doppio combat
    if player.get("target") or mob.get("target"):
        return

    player["target"] = mob
    mob["target"] = player

    # assicura conn aggiornata
    player["conn"] = conn

    if conn:
        conn.send(f"Attacchi {mob['name']}!\n")


# =========================
# PLAYER ATTACK
# =========================
def player_attack(player, mob):

    conn = player.get("conn")
    if not conn:
        return

    if mob.get("hp", 0) <= 0:
        return

    # miss
    if random.random() < 0.1:
        conn.send("Mancato!\n")
        return

    # critico
    crit = random.random() < 0.1
    dmg = player.get("damage", 1)

    if crit:
        dmg *= 2
        conn.send("Colpo critico!\n")

    mob["hp"] -= dmg

    conn.send(f"Colpisci {mob['name']} per {dmg} danni.\n")

    if mob["hp"] <= 0:
        handle_mob_death(player, mob)


# =========================
# MOB ATTACK (AI)
# =========================
def mob_attack(mob, player):

    conn = player.get("conn")
    if not conn:
        return

    if player.get("hp", 0) <= 0:
        return

    if random.random() < 0.1:
        conn.send(f"{mob['name']} manca il colpo.\n")
        return

    dmg = mob.get("damage", 1)

    player["hp"] -= dmg

    conn.send(f"{mob['name']} ti colpisce per {dmg} danni.\n")

    if player["hp"] <= 0:
        handle_player_death(player)


# =========================
# MORTE MOB
# =========================
def handle_mob_death(player, mob):

    conn = player.get("conn")
    room = rooms.get(player.get("room"))

    print(f"[DEATH] Creato corpse per {mob['name']}")

    # -------------------------
    # RIMOZIONE MOB
    # -------------------------
    if room and mob in room.mobs:
        room.mobs.remove(mob)

    # reset combat
    player["target"] = None
    mob["target"] = None

    # -------------------------
    # REWARD BASE
    # -------------------------
    xp = mob.get("xp", 10)
    gold = mob.get("gold", random.randint(1, 10))

    player["xp"] = player.get("xp", 0) + xp
    player["gold"] = player.get("gold", 0) + gold

    if conn:
        conn.send(f"Ottieni {xp} XP e {gold} oro.\n")

    print(f"[GOLD] {player['name']} +{gold} (tot={player['gold']})")

    # -------------------------
    # DROP ITEM
    # -------------------------
    if room:
        drop = mob.get("drop")

        if drop:
            try:
                room.items.append(drop.copy())
                print(f"[DROP] {drop.get('name')}")
            except:
                print("[DROP ERROR]")

    # -------------------------
    # QUEST SYSTEM (MIGLIORATO)
    # -------------------------
    quest = player.get("quest")

    if quest and not quest.get("completed"):

        target = quest.get("target")
        mob_name = mob.get("name")

        if mob_name == target:

            quest["progress"] = quest.get("progress", 0) + 1

            if conn:
                conn.send(
                    f"[QUEST] {quest['progress']}/{quest['required']} {target} uccisi\n"
                )

            # completamento
            if quest["progress"] >= quest["required"]:
                quest["completed"] = True

                if conn:
                    conn.send("[QUEST] COMPLETATA! Torna dal locandiere.\n")

    # -------------------------
    # BROADCAST
    # -------------------------
    if room:
        broadcast_room(
            room,
            f"{mob['name']} è stato ucciso.\n",
            exclude=player
        )


# =========================
# MORTE PLAYER
# =========================
def handle_player_death(player):

    conn = player.get("conn")

    player["hp"] = player.get("max_hp", 100)
    player["target"] = None

    if conn:
        conn.send("Sei morto! Torni alla locanda.\n")

    # respawn
    player["room"] = player.get("start_room", 1001)


# =========================
# LOOP COMBAT
# =========================
def combat_tick():

    for room in rooms.values():

        # sicurezza
        if not hasattr(room, "mobs"):
            continue

        for mob in list(room.mobs):

            target = mob.get("target")

            if target:
                mob_attack(mob, target)