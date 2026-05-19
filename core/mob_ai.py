import asyncio
import random
import traceback

from core.world import rooms
from core.combat_system import start_combat


# =====================================
# GET AI COMPONENT
# =====================================

def get_ai(mob):

    return mob.get(
        "components",
        {}
    ).get(
        "AIComponent"
    )


# =====================================
# GET POSITION COMPONENT
# =====================================

def get_position(mob):

    return mob.get(
        "components",
        {}
    ).get(
        "PositionComponent"
    )


# =====================================
# SAFE TARGET ID
# =====================================

def get_entity_id(entity):

    if not entity:
        return None

    return entity.get(
        "entity_id",
        entity.get(
            "name",
            "unknown"
        )
    )


# =====================================
# MAIN AI LOOP
# =====================================

async def mob_ai_loop():

    print("[AI LOOP AVVIATO]")

    while True:

        try:

            for room in rooms.values():

                # sicurezza
                if not hasattr(room, "mobs"):
                    continue

                # copia safe
                for mob in list(room.mobs):

                    try:

                        # =========================
                        # DEBUG
                        # =========================

                        print(
                            f"[AI DEBUG] "
                            f"{mob['name']} | "
                            f"ecs={'components' in mob}"
                        )

                        # =========================
                        # COMPONENTS
                        # =========================

                        ai = get_ai(mob)

                        position = get_position(mob)

                        # =========================
                        # POSITION SYNC
                        # =========================

                        if position:

                            position.room_id = (
                                room.vnum
                            )

                        # =========================
                        # TARGET
                        # =========================

                        target = mob.get("target")

                        # ECS sync
                        if ai:

                            ai.target = target

                            # SAFE TARGET ID
                            if target:

                                ai.memory[
                                    "target_id"
                                ] = get_entity_id(
                                    target
                                )

                        # =========================
                        # TARGET DEAD
                        # =========================

                        if target:

                            target_hp = target.get(
                                "hp",
                                target.get(
                                    "current_hp",
                                    1
                                )
                            )

                            if target_hp <= 0:

                                mob["target"] = None

                                if ai:

                                    ai.target = None

                                    ai.state = "idle"

                                continue

                        # =========================
                        # COMBAT
                        # =========================

                        if target:

                            if ai:
                                ai.state = "combat"

                            start_combat(
                                target,
                                mob,
                                target.get("conn")
                            )

                            continue

                        # =========================
                        # IDLE
                        # =========================

                        if ai:
                            ai.state = "idle"

                        # =========================
                        # RANDOM MOVE
                        # =========================

                        if random.random() < 0.05:

                            exits = list(
                                room.exits.keys()
                            )

                            if exits:

                                direction = (
                                    random.choice(
                                        exits
                                    )
                                )

                                exit_data = room.exits.get(
                                    direction
                                )

                                # =========================
                                # SIMPLE EXIT
                                # =========================

                                if isinstance(
                                   exit_data,
                                   int
                                ):

                                   next_room_vnum = exit_data

                                #  =========================
                                # ADVANCED EXIT
                                # =========================

                                elif isinstance(
                                   exit_data,
                                   dict
                                ):

                                    next_room_vnum = exit_data.get(
                                        "to"
                                    )

                                else:

                                    continue

                                next_room = rooms.get(
                                    next_room_vnum
                                )

                                if next_room:

                                    # remove
                                    if mob in room.mobs:
                                        room.mobs.remove(mob)

                                    # add
                                    next_room.mobs.append(
                                        mob
                                    )

                                    # legacy sync
                                    mob["room"] = (
                                        next_room.vnum
                                    )

                                    # ECS sync
                                    if position:

                                        position.last_room_id = (
                                            position.room_id
                                        )

                                        position.room_id = (
                                            next_room.vnum
                                        )

                                    print(
                                        f"[AI MOVE] "
                                        f"{mob['name']} "
                                        f"-> "
                                        f"{next_room.vnum}"
                                    )

                    except Exception as e:

                        print(
                            f"[AI ERROR] {e}"
                        )

                        traceback.print_exc()

        except Exception as e:

            print(
                f"[AI LOOP ERROR] {e}"
            )

            traceback.print_exc()

        await asyncio.sleep(2)