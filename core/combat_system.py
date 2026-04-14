import asyncio
from core.xp_system import add_xp


async def send(player, msg):
    writer = player.get("writer")
    if writer:
        writer.write((msg + "\n").encode())
        await writer.drain()


async def start_combat(player, target):
    room = player.get("room")

    await send(player, f"Inizi il combattimento con {target['name']}!")

    while player["hp"] > 0 and target["hp"] > 0:

        # =========================
        # 🗡️ PLAYER ATTACCA
        # =========================
        dmg = 5

        weapon = player.get("equipment", {}).get("weapon")
        if weapon:
            dmg += weapon.get("damage", 0)

        target["hp"] -= dmg

        await send(player, f"Colpisci {target['name']} per {dmg} danni!")

        if target["hp"] <= 0:
            await send(player, f"{target['name']} muore!")

            # 💀 corpse
            corpse = {
                "name": f"corpo di {target['name']}",
                "description": f"Il corpo senza vita di {target['name']}.",
                "type": "corpse",
                "inventory": target.get("inventory", [])
            }

            if not hasattr(room, "items"):
                room.items = []

            room.items.append(corpse)

            if target in room.mobs:
                room.mobs.remove(target)

            # ⭐ XP
            xp = target.get("xp", 10)
            await add_xp(player, xp)

            return

        # =========================
        # 👹 MOB ATTACCA
        # =========================
        dmg = 3
        player["hp"] -= dmg

        await send(player, f"{target['name']} ti colpisce per {dmg} danni!")

        if player["hp"] <= 0:
            await send(player, "Sei morto!")
            return

        await asyncio.sleep(2)