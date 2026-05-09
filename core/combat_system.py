import random
import time

from core.world import rooms, broadcast_room

from systems.stat_system import StatSystem
from systems.aggro_system import add_aggro


# =====================================
# STAT SYSTEM
# =====================================

stat_system = StatSystem()


# =====================================
# GET COMPONENT
# =====================================

def get_component(entity, name):

    return entity.get(
        "components",
        {}
    ).get(name)


# =====================================
# START COMBAT
# =====================================

def start_combat(player, mob, conn):

    if not player or not mob:
        return

    if not player.get("alive", True):
        return

    if not mob.get("alive", True):
        return

    if player.get("target") or mob.get("target"):
        return

    player["target"] = mob
    mob["target"] = player

    player["conn"] = conn

    player_combat = get_component(
        player,
        "CombatComponent"
    )

    mob_combat = get_component(
        mob,
        "CombatComponent"
    )

    if player_combat:

        player_combat.in_combat = True

        player_combat.target_id = mob.get(
            "entity_id"
        )

    if mob_combat:

        mob_combat.in_combat = True

        mob_combat.target_id = player.get(
            "entity_id"
        )

    add_aggro(
        mob,
        player,
        1
    )

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

    if not mob.get("alive", True):
        return

    if stat_system.get_hp(mob) <= 0:
        return

    combat = get_component(
        player,
        "CombatComponent"
    )

    if combat and combat.stunned:

        conn.send(
            "Sei stordito!\n"
        )

        return

    if combat:

        now = time.time()

        if (
            now - combat.last_attack_time
            < combat.attack_cooldown
        ):
            return

        combat.last_attack_time = now

    if random.random() < 0.1:

        conn.send(
            "Mancato!\n"
        )

        return

    crit = random.random() < 0.1

    attack = stat_system.get_attack(
        player
    )

    defense = stat_system.get_defense(
        mob
    )

    dmg = max(
        1,
        attack - defense
    )

    if crit:

        dmg *= 2

        conn.send(
            "Colpo critico!\n"
        )

    stat_system.damage(
        mob,
        dmg
    )

    add_aggro(
        mob,
        player,
        dmg
    )

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

    if not mob.get("alive", True):
        return

    if not player.get("alive", True):
        return

    if stat_system.get_hp(player) <= 0:
        return

    combat = get_component(
        mob,
        "CombatComponent"
    )

    if combat and combat.stunned:
        return

    if combat:

        now = time.time()

        if (
            now - combat.last_attack_time
            < combat.attack_cooldown
        ):
            return

        combat.last_attack_time = now

    if random.random() < 0.1:

        conn.send(
            f"{mob['name']} "
            f"manca il colpo.\n"
        )

        return

    attack = stat_system.get_attack(
        mob
    )

    defense = stat_system.get_defense(
        player
    )

    dmg = max(
        1,
        attack - defense
    )

    stat_system.damage(
        player,
        dmg
    )

    hp = stat_system.get_hp(
        player
    )

    conn.send(
        f"{mob['name']} "
        f"ti colpisce "
        f"per {dmg} danni.\n"
    )

    conn.send(
        f"HP: {hp}/"
        f"{stat_system.get_max_hp(player)}\n"
    )

    if hp <= 0:

        handle_player_death(
            player
        )


# =====================================
# HANDLE MOB DEATH
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

    mob["alive"] = False

    mob["target"] = None

    combat = get_component(
        mob,
        "CombatComponent"
    )

    if combat:

        combat.in_combat = False

        combat.target_id = None

    threat = get_component(
        mob,
        "ThreatComponent"
    )

    if threat:

        threat.clear()

    ai = get_component(
        mob,
        "AIComponent"
    )

    if ai:

        ai.target = None

        ai.state = "dead"

    player["target"] = None

    player_combat = get_component(
        player,
        "CombatComponent"
    )

    if player_combat:

        player_combat.in_combat = False

        player_combat.target_id = None

    if room and mob in room.mobs:

        room.mobs.remove(mob)

    # =================================
    # REWARDS
    # =================================

    xp = mob.get("xp", 10)

    gold = random.randint(
        mob.get("gold_min", 1),
        mob.get("gold_max", 10)
    )

    player["xp"] = (
        player.get("xp", 0)
        + xp
    )

    # =================================
    # MESSAGGI
    # =================================

    if conn:

        conn.send(
            f"{mob['name']} "
            f"è stato sconfitto!\n"
        )

    # =================================
    # QUEST
    # =================================

    quest = player.get("quest")

    if quest and not quest.get(
        "completed"
    ):

        target = quest.get("target")

        if mob.get("name") == target:

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

            if (
                quest["progress"]
                >= quest["required"]
            ):

                quest["completed"] = True

                if conn:

                    conn.send(
                        "[QUEST] "
                        "COMPLETATA!\n"
                    )

    # =================================
    # CORPSE
    # =================================

    if room:

        corpse = {

            "name": f"corpo di {mob['name']}",

            "description":
                f"Il corpo senza vita di "
                f"{mob['name']}.",

            "loot":
                mob.get("loot", []),

            "gold":
                gold
        }

        room.items.append(corpse)

    # =================================
    # BROADCAST
    # =================================

    if room:

        broadcast_room(
            room,
            f"{mob['name']} "
            f"è stato ucciso.\n",
            exclude=player
        )


# =====================================
# HANDLE PLAYER DEATH
# =====================================

def handle_player_death(player):

    conn = player.get("conn")

    player["alive"] = False

    combat = get_component(
        player,
        "CombatComponent"
    )

    if combat:

        combat.in_combat = False

        combat.target_id = None

    max_hp = stat_system.get_max_hp(
        player
    )

    player["hp"] = max_hp

    player["current_hp"] = max_hp

    player["target"] = None

    player["room"] = player.get(
        "start_room",
        1001
    )

    player["alive"] = True

    if conn:

        conn.send(
            "Sei morto! "
            "Torni alla locanda.\n"
        )


# =====================================
# COMBAT LOOP
# =====================================

def combat_tick():

    for room in rooms.values():

        if not hasattr(room, "mobs"):
            continue

        for mob in list(room.mobs):

            try:

                if not mob.get(
                    "alive",
                    True
                ):
                    continue

                target = mob.get(
                    "target"
                )

                if not target:
                    continue

                if not target.get(
                    "alive",
                    True
                ):

                    mob["target"] = None

                    continue

                player_attack(
                    target,
                    mob
                )

                if not mob.get(
                    "alive",
                    True
                ):
                    continue

                mob_attack(
                    mob,
                    target
                )

            except Exception as e:

                print(
                    f"[COMBAT ERROR] {e}"
                )