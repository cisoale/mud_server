import asyncio
import random
from core.combat_utils import (
    create_corpse,
    get_total_damage,
    get_total_armor
)


async def combat_loop(player, conn):
    while True:
        combat = player.get("combat", {})

        # 🔒 sicurezza stato
        if not combat.get("in_combat"):
            break

        target = combat.get("target")

        if not target:
            await conn.send("Il combattimento si interrompe.")
            combat["in_combat"] = False
            break

        room = player.get("room")

        # ❌ target non più valido
        if target not in room.mobs:
            await conn.send("Il bersaglio non è più qui.")
            combat["in_combat"] = False
            break

        # =========================
        # ⚔️ PLAYER ATTACCA
        # =========================
        base_damage = get_total_damage(player)
        dmg = random.randint(base_damage, base_damage + 2)

        target["hp"] -= dmg

        await conn.send(f"Colpisci {target['name']} per {dmg} danni.")

        # 💀 MORTE MOB
        if target["hp"] <= 0:
            await conn.send(f"Hai ucciso {target['name']}!")

            # rimuovi mob
            if target in room.mobs:
                room.mobs.remove(target)

            # crea corpse
            corpse = create_corpse(target)
            room.items.append(corpse)

            # 🎁 XP
            xp = target.get("xp", 0)
            player["xp"] += xp

            await conn.send(f"Ottieni {xp} XP.")

            from core.database import save_player
            save_player(player)

            # 🔥 LEVEL UP
            if player["xp"] >= player["xp_to_next"]:
                player["level"] += 1
                player["xp"] -= player["xp_to_next"]
                player["xp_to_next"] = int(player["xp_to_next"] * 1.5)

                player["max_hp"] += 5
                player["hp"] = player["max_hp"]

                await conn.send(f"🔥 LEVEL UP! Ora sei livello {player['level']}!")

            # stop combat
            combat["in_combat"] = False
            combat["target"] = None
            break

        # =========================
        # 👹 MOB ATTACCA
        # =========================
        base_mob_damage = random.randint(1, 4)
        armor = get_total_armor(player)

        dmg = max(0, base_mob_damage - armor)

        player["hp"] -= dmg

        if armor > 0:
            await conn.send(
                f"{target['name']} ti colpisce per {dmg} danni (ridotto da armatura)."
            )
        else:
            await conn.send(
                f"{target['name']} ti colpisce per {dmg} danni."
            )

        # 💀 MORTE PLAYER
        if player["hp"] <= 0:
            await conn.send("💀 Sei morto!")

            # respawn semplice
            player["hp"] = player["max_hp"]

            combat["in_combat"] = False
            combat["target"] = None
            break

        # =========================
        # ⏱ ATTESA TURNO
        # =========================
        await asyncio.sleep(2)