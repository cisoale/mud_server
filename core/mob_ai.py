from core.combat_system import start_combat
from core.world import rooms
import asyncio
import random

print("USANDO QUESTO MOB_AI:", __file__)
async def mob_ai_loop():
    import inspect
    print("LINE:", inspect.getsource(mob_ai_loop))
    while True:
        await asyncio.sleep(2)

        for room in list(rooms.values()):

            # sicurezza
            if not hasattr(room, "players") or not hasattr(room, "mobs"):
                continue

            if not room.players:
                continue

            for mob in list(room.mobs):

                # solo aggressivi
                if not mob.get("aggressive"):
                    continue

                # 🔥 FIX SPAM: se già in combat
                if mob.get("target"):
                    continue

                # scegli player
                player = random.choice(room.players)

                # 🔥 FIX: se player già in combat
                if player.get("target"):
                    continue

                print(f"[AI] {mob['name']} attacca {player['name']}")

                try:
                    start_combat(player, mob, player["conn"])
                except Exception as e:
                    print("[ERRORE AI]", e)