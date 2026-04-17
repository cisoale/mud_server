import asyncio
from core.world import rooms
from core.combat_system import start_combat


async def mob_ai_loop():

    while True:

        for room in rooms.values():

            # sicurezza
            if not hasattr(room, "mobs") or not hasattr(room, "players"):
                continue

            for mob in room.mobs:

                # sicurezza
                if not isinstance(mob, dict):
                    continue

                # -------------------------
                # MOB AGGRESSIVO
                # -------------------------
                if mob.get("aggressive"):

                    if room.players:

                        target = room.players[0]

                        # evita spam combat
                        if target.get("in_combat"):
                            continue

                        print(f"[AI] {mob['name']} attacca {target['name']}")

                        # ⚔️ attacco automatico
                        start_combat(target, mob, target.get("conn"))

        await asyncio.sleep(3)