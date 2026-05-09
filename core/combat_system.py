import random

from core.world import rooms, broadcast_room

from systems.stat_system import StatSystem


# =====================================
# STAT SYSTEM
# =====================================

stat_system = StatSystem()


# =====================================
# START COMBAT
# =====================================

def start_combat(player, mob, conn):

    # evita doppio combat
    if player.get("target") or mob.get("target"):
        return

    player["target"] = mob
    mob["target"] = player

    # aggiorna conn
    player["conn"] = conn

    if conn:
        conn.send(
            f"Attacchi {mob['name']}!\n"
        )


# =====================================
# PLAYER ATTACK
# =====================================

def player_attack(player, mob):

    conn = player.get("conn")

    if not conn:
        return

    # sicurezza hp
    if stat_system.get_hp(mob) <= 0:
        return

    # =========================
    # MISS
    # =========================

    if random.random() < 0.1:

        conn.send("Mancato!\n")

        return

    # =========================
    # CRIT
    # =========================

    crit = random.random() < 0.1

    # =========================
    # ECS DAMAGE
    # =========================

    attack = stat_system.get_attack(player)

    defense = stat_system.get_defense(mob)

    dmg = max(1, attack - defense)

    if crit:

        dmg *= 2

        conn.send(
            "Colpo critico!\n"
        )

    # applica danno ECS
    stat_system.damage(
        mob,
        dmg
    )

    # sync hp
    hp = stat_system.get_hp(mob)

    conn.send(
        f"Colpisci "
        f"{mob['name']} "
        f"per {dmg} danni.\n"
    )

    conn.send(
        f"{mob['name']} "
        f"HP: {hp}\n"
    )

    # =========================
    # MORTE
    # =========================

    if hp <= 0:

        handle_mob_death(
            player,
            mob
        )


# =====================================
# MOB ATTACK
# =====================================

def mob_attack(mob, player):

    conn = player.get("conn")

    if not conn:
        return

    # sicurezza hp
    if stat_system.get_hp(player) <= 0:
        return

    # =========================
    # MISS
    # =========================

    if random.random() < 0.1:

        conn.send(
            f"{mob['name']} "
            f"manca il colpo.\n"
        )

        return

    # =========================
    # DAMAGE
    # =========================

    attack = stat_system.get_attack(mob)

    defense = stat_system.get_defense(player)

    dmg = max(1, attack - defense)

    # applica danno ECS
    stat_system.damage(
        player,
        dmg
    )

    hp = stat_system.get_hp(player)

    conn.send(
        f"{mob['name']} "
        f"ti colpisce "
        f"per {dmg} danni.\n"
    )

    conn.send(
        f"HP: {hp}/"
        f"{stat_system.get_max_hp(player)}\n"
    )

    # =========================
    # MORTE
    # =========================

    if hp <= 0:

        handle_player_death(
            player
        )


# =====================================
# MORTE MOB
# =====================================

def handle_mob_death(player, mob):

    conn = player.get("conn")

    room = rooms.get(
        player.get("room")
    )

    print(
        f"[DEATH] "
        f"{mob['name']} morto"
    )

    # =========================
    # REMOVE MOB
    # =========================

    if room and mob in room.mobs:

        room.mobs.remove(mob)

    # =========================
    # RESET TARGETS
    # =========================

    player["target"] = None
    mob["target"] = None

    # =========================
    # REWARDS
    # =========================

    xp = mob.get("xp", 10)

    gold = mob.get(
        "gold",
        random.randint(1, 10)
    )

    player["xp"] = (
        player.get("xp", 0)
        + xp
    )

    player["gold"] = (
        player.get("gold", 0)
        + gold
    )

    if conn:

        conn.send(
            f"Ottieni "
            f"{xp} XP "
            f"e {gold} oro.\n"
        )

    print(
        f"[GOLD] "
        f"{player['name']} "
        f"+{gold} "
        f"(tot={player['gold']})"
    )

    # =========================
    # DROP
    # =========================

    if room:

        drop = mob.get("drop")

        if drop:

            try:

                room.items.append(
                    drop.copy()
                )

                print(
                    f"[DROP] "
                    f"{drop.get('name')}"
                )

            except Exception as e:

                print(
                    f"[DROP ERROR] {e}"
                )

    # =========================
    # QUEST SYSTEM
    # =========================

    quest = player.get("quest")

    if quest and not quest.get(
        "completed"
    ):

        target = quest.get("target")

        mob_name = mob.get("name")

        if mob_name == target:

            quest["progress"] = (
                quest.get(
                    "progress",
                    0
                ) + 1
            )

            if conn:

                conn.send(
                    f"[QUEST] "
                    f"{quest['progress']}/"
                    f"{quest['required']} "
                    f"{target} uccisi\n"
                )

            # completamento
            if (
                quest["progress"]
                >= quest["required"]
            ):

                quest["completed"] = True

                if conn:

                    conn.send(
                        "[QUEST] "
                        "COMPLETATA! "
                        "Torna dal locandiere.\n"
                    )

    # =========================
    # BROADCAST
    # =========================

    if room:

        broadcast_room(
            room,
            f"{mob['name']} "
            f"è stato ucciso.\n",
            exclude=player
        )


# =====================================
# MORTE PLAYER
# =====================================

def handle_player_death(player):

    conn = player.get("conn")

    # reset hp
    max_hp = stat_system.get_max_hp(
        player
    )

    player["hp"] = max_hp

    if "current_hp" in player:
        player["current_hp"] = max_hp

    player["target"] = None

    if conn:

        conn.send(
            "Sei morto! "
            "Torni alla locanda.\n"
        )

    # respawn
    player["room"] = player.get(
        "start_room",
        1001
    )


# =====================================
# COMBAT LOOP
# =====================================

def combat_tick():

    for room in rooms.values():

        # sicurezza
        if not hasattr(room, "mobs"):
            continue

        for mob in list(room.mobs):

            target = mob.get("target")

            if target:

                try:

                    mob_attack(
                        mob,
                        target
                    )

                except Exception as e:

                    print(
                        f"[COMBAT ERROR] {e}"
                    )