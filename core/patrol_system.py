import asyncio
from core.world import get_room, broadcast_room


# =========================
# LOOP PRINCIPALE
# =========================
async def patrol_loop():
    while True:

        from core.world import rooms

        for room in rooms.values():
            for mob in list(room.mobs):

                if mob.get("ai") != "patrol":
                    continue

                handle_patrol(mob)

        await asyncio.sleep(2)


# =========================
# LOGICA PATROL
# =========================
def handle_patrol(mob):

    # NON muovere se in combat
    if mob.get("target"):
        return

    route = mob.get("patrol_route")
    if not route:
        return

    # init valori runtime
    mob.setdefault("patrol_index", 0)
    mob.setdefault("patrol_timer", 0)

    mob["patrol_timer"] += 1

    delay = mob.get("patrol_delay", 5)

    if mob["patrol_timer"] < delay:
        return

    mob["patrol_timer"] = 0

    current_room = get_room(mob.get("room"))
    if not current_room:
        return

    # prossimo step
    mob["patrol_index"] = (mob["patrol_index"] + 1) % len(route)
    next_room_id = route[mob["patrol_index"]]

    next_room = get_room(next_room_id)
    if not next_room:
        return

    # rimuovi da stanza attuale
    if mob in current_room.mobs:
        current_room.mobs.remove(mob)

    # aggiungi alla nuova
    next_room.mobs.append(mob)
    mob["room"] = next_room.vnum

    # messaggi
    broadcast_room(current_room, f"{mob['name']} si allontana.\n")
    broadcast_room(next_room, f"{mob['name']} entra nella stanza.\n")