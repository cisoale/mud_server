import asyncio
import random
import os
import json

from core.world import get_room
from core.save_system import save_player
from core.death_system import handle_death
from core.mob_loader import create_mob
from core.combat_boss import boss_action

# opzionale Lua
try:
    from core.lua_engine import run_lua
except ImportError:
    run_lua = None


# =========================
# CONFIG
# =========================
ITEMS_PATH = "data/items"
MAX_MOBS_PER_ROOM = 5
COMBAT_TICK = 2


# =========================
# UTILS
# =========================
def broadcast_room(room, message, exclude=None):
    """Invia un messaggio a tutti i player nella stanza."""
    for p in room.players:
        if exclude and p == exclude:
            continue

        conn = p.get("conn")
        if conn:
            conn.send(message)


def get_item_data(name):
    """Carica i dati di un item dal filesystem."""
    path = os.path.join(ITEMS_PATH, f"{name}.json")

    if not os.path.exists(path):
        return {}

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def rarity_color(name, rarity):
    """Restituisce nome item con colore rarità."""
    colors = {
        "common": "",
        "uncommon": "[Verde] ",
        "rare": "[Blu] ",
        "epic": "[Viola] ",
        "legendary": "[Oro] "
    }
    return f"{colors.get(rarity, '')}{name}"


# =========================
# DAMAGE SYSTEM
# =========================
def calculate_damage(attacker, defender):
    """Calcola il danno tra due entità."""

    base = attacker.get("damage", 2)

    from core.equipment_system import get_equipment_bonus

    bonus = get_equipment_bonus(attacker)
    base += bonus["damage"]

    defense = defender.get("defense", 0) + get_equipment_bonus(defender)["defense"]

    defense = defender.get("defense", 0)
    dmg = max(1, base - defense)

    # crit bilanciato
    if random.random() < 0.05:
        dmg = int(dmg * 1.5)

    return dmg


# =========================
# LOOT SYSTEM
# =========================
def generate_loot_lua(mob):
    """Genera loot tramite script Lua."""

    if not run_lua:
        return []

    script = mob.get("loot_script")
    if not script:
        return []

    result = run_lua(script, "")

    if not result:
        return []

    loot = []

    for entry in result.split(","):
        try:
            name, qty = entry.split(":")
            loot.append({
                "name": name.strip(),
                "quantity": int(qty)
            })
        except Exception:
            continue

    return loot


def generate_loot_json(mob):
    """Genera loot tramite configurazione JSON."""

    loot = []

    for entry in mob.get("loot", []):

        chance = entry.get("chance", 0)
        rarity = entry.get("rarity", "common")

        # modifica probabilità per rarità
        if rarity == "rare":
            chance *= 0.8
        elif rarity == "epic":
            chance *= 0.5
        elif rarity == "legendary":
            chance *= 0.2

        if random.random() <= chance:

            qty = random.randint(
                entry.get("min", 1),
                entry.get("max", 1)
            )

            loot.append({
                "name": entry.get("item"),
                "quantity": qty
            })

    return loot


def process_loot(mob, room):
    """Applica il loot nella stanza e lo mostra."""

    loot = generate_loot_lua(mob) or generate_loot_json(mob)

    for item in loot:
        item_data = get_item_data(item["name"])

        rarity = item_data.get("rarity", "common")
        display_name = item_data.get("display_name", item["name"])

        display_name = rarity_color(display_name, rarity)

        room.items.append(item)

        broadcast_room(
            room,
            f"{mob['name']} lascia {item['quantity']}x {display_name}.\n"
        )


# =========================
# RESPAWN SYSTEM
# =========================
async def respawn_mob(room, mob_name, delay=10):
    await asyncio.sleep(delay)

    if len(room.mobs) >= MAX_MOBS_PER_ROOM:
        return

    mob = create_mob(mob_name)

    if mob:
        room.mobs.append(mob)
        broadcast_room(room, f"{mob_name} appare nella stanza.\n")


# =========================
# START COMBAT
# =========================
def start_combat(player, mob, conn):
    """Avvia il combattimento tra player e mob."""

    room = get_room(player["room"])
    if not room:
        print("[ERRORE COMBAT] room non trovata")
        return

    if player.get("target") or mob.get("target"):
        return

    player.setdefault("current_hp", player.get("hp", 100))
    mob.setdefault("current_hp", mob.get("hp", 20))

    player["target"] = mob
    mob["target"] = player

    conn.send(f"Inizia il combattimento con {mob['name']}!\n")

    broadcast_room(
        room,
        f"{player['name']} attacca {mob['name']}!\n",
        exclude=player
    )

    asyncio.create_task(combat_loop(player, mob))


# =========================
# COMBAT LOOP
# =========================
async def combat_loop(player, mob):

    while True:

        await asyncio.sleep(COMBAT_TICK)

        room = get_room(player["room"])
        if not room:
            return

        if mob not in room.mobs or player not in room.players:
            return

        # PLAYER ATTACK
        dmg = calculate_damage(player, mob)
        mob["current_hp"] -= dmg

        broadcast_room(
            room,
            f"{player['name']} colpisce {mob['name']} ({mob['current_hp']} HP) per {dmg} danni!\n"
        )

        if mob["current_hp"] <= 0:
            handle_mob_death(player, mob, room)
            return

        # MOB ATTACK
        msg = boss_action(mob, player)

        if msg:
            broadcast_room(room, msg + "\n")
        else:
            dmg = calculate_damage(mob, player)
            player["current_hp"] -= dmg

            broadcast_room(
                room,
                f"{mob['name']} colpisce {player['name']} per {dmg} danni!\n"
            )

        if player["current_hp"] <= 0:
            handle_player_death(player, room)
            return


# =========================
# MOB MORTE
# =========================
def handle_mob_death(player, mob, room):

    broadcast_room(room, f"{mob['name']} muore!\n")

    # XP
    xp = mob.get("xp", 10)
    player["xp"] = player.get("xp", 0) + xp

    if player.get("conn"):
        player["conn"].send(f"Hai guadagnato {xp} XP!\n")

    from core.xp_system import check_level_up
    check_level_up(player, player.get("conn"))

    # GOLD + CORPSE
    handle_death(player, mob, room, broadcast_room)

    # LOOT
    process_loot(mob, room)

    # REMOVE
    if mob in room.mobs:
        room.mobs.remove(mob)

    # RESPAWN
    asyncio.create_task(respawn_mob(room, mob["name"], delay=10))

    player["target"] = None
    mob["target"] = None

    save_player(player)


# =========================
# PLAYER MORTE
# =========================
def handle_player_death(player, room):

    broadcast_room(room, f"{player['name']} è morto!\n")

    player["current_hp"] = player.get("hp", 100)
    player["room"] = 1001
    player["target"] = None

    conn = player.get("conn")
    if conn:
        conn.send("Sei morto! Torni al punto di partenza.\n")

    save_player(player)