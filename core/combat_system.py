import asyncio
import random

from core.world import get_room
from core.xp_system import add_xp
from core.equipment_system import get_weapon_damage, get_total_armor
from core.crit_system import calculate_crit, apply_crit
from core.save_system import auto_save

def start_combat(player, mob, conn):
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(combat_loop(player, mob, conn))
# =========================
# LOOP COMBAT
# =========================
async def combat_loop(player, mob, conn):

    conn.send(f"Inizi il combattimento contro {mob['name']}!\n")

    while True:

        # =========================
        # PLAYER ATTACCA
        # =========================
        base = random.randint(3, 6)
        str_bonus = player.get("str", 10) // 2
        weapon_bonus = get_weapon_damage(player)

        dmg = base + str_bonus + weapon_bonus

        # CRIT
        if calculate_crit(player):
            dmg = apply_crit(dmg)
            conn.send("💥 COLPO CRITICO!\n")

        mob["hp"] -= dmg

        conn.send(
            f"Colpisci {mob['name']} per {dmg} danni "
            f"(arma:{weapon_bonus} STR:{str_bonus}).\n"
        )

        # =========================
        # MORTE MOB
        # =========================
        if mob["hp"] <= 0:

            conn.send(f"Hai ucciso {mob['name']}!\n")

            # XP
            xp = mob.get("xp", 10)
            add_xp(player, xp, conn)

            room = get_room(player["room"])
            player["in_combat"] = False
            # CREA CORPO
            corpse = {
                "name": f"corpo di {mob['name']}",
                "type": "corpse",
                "inventory": mob.get("inventory", [])
            }

            if not hasattr(room, "items"):
                room.items = []

            room.items.append(corpse)

            # RIMUOVI MOB
            if hasattr(room, "mobs"):
                room.mobs = [m for m in room.mobs if m != mob]

            conn.send(f"Il corpo di {mob['name']} cade a terra.\n")

            auto_save(player)
            return

        # =========================
        # MOB ATTACCA
        # =========================
        base = random.randint(3, 8)
        armor = get_total_armor(player)

        dmg = max(1, base - armor)

        player["hp"] -= dmg

        conn.send(
            f"{mob['name']} ti colpisce per {dmg} danni "
            f"(armatura:{armor}).\n"
        )

        # =========================
        # MORTE PLAYER
        # =========================
        if player["hp"] <= 0:

            conn.send("💀 Sei morto!\n")
            player["in_combat"] = False
            player["hp"] = player.get("max_hp", 100)
            player["room"] = 1001

            conn.send("Sei stato respawnato.\n")

            auto_save(player)
            return

        await asyncio.sleep(2)


# =========================
# START COMBAT
# =========================
def start_combat(player, mob, conn):

    if "hp" not in mob:
        mob["hp"] = mob.get("max_hp", 20)

    asyncio.create_task(combat_loop(player, mob, conn))