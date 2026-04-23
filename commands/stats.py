from core.stats import get_total_stats, get_weapon_damage, get_total_defense
from core.set_bonus import get_set_bonus
from core.effects import get_item_effects


def execute(player, conn, args):

    # =========================
    # DATI BASE
    # =========================
    name = player.get("name", "???")
    level = player.get("level", 1)
    xp = player.get("xp", 0)
    hp = player.get("hp", 0)

    base_stats = player.get("stats", {})
    total_stats = get_total_stats(player)

    equipment = player.get("equipment", {})

    # =========================
    # HEADER
    # =========================
    conn.send("\n=========================\n")
    conn.send(f" {name.upper()} - LIVELLO {level}\n")
    conn.send("=========================\n")

    # =========================
    # RISORSE
    # =========================
    conn.send(f"HP: {hp}\n")
    conn.send(f"XP: {xp}\n")

    # =========================
    # STATISTICHE
    # =========================
    conn.send("\n--- STATISTICHE ---\n")

    for stat in ["str", "dex", "int"]:

        base = base_stats.get(stat, 0)
        total = total_stats.get(stat, 0)
        bonus = total - base

        if bonus > 0:
            conn.send(f"{stat.upper()}: {total} (+{bonus})\n")
        else:
            conn.send(f"{stat.upper()}: {total}\n")

    # =========================
    # COMBAT
    # =========================
    damage = get_weapon_damage(player)
    defense = get_total_defense(player)

    conn.send("\n--- COMBATTIMENTO ---\n")
    conn.send(f"Danno: {damage}\n")
    conn.send(f"Difesa: {defense}\n")

    # =========================
    # EQUIPAGGIAMENTO
    # =========================
    conn.send("\n--- EQUIPAGGIAMENTO ---\n")

    slots = [
        "testa", "torso", "gambe", "piedi",
        "mani", "arma", "secondaria",
        "anello1", "anello2", "collo"
    ]

    for slot in slots:
        item = equipment.get(slot)

        if item:
            conn.send(f"{slot.capitalize()}: {item.get('name', '???')}\n")
        else:
            conn.send(f"{slot.capitalize()}: ---\n")

    # =========================
    # BONUS SET
    # =========================
    set_bonus = get_set_bonus(player)

    if set_bonus:
        conn.send("\n--- BONUS SET ---\n")
        for stat, value in set_bonus.items():
            conn.send(f"{stat.upper()}: +{value}\n")

    # =========================
    # EFFETTI ATTIVI
    # =========================
    effects = get_item_effects(player)

    if effects:
        conn.send("\n--- EFFETTI ATTIVI ---\n")
        for effect, value in effects.items():
            conn.send(f"{effect}: {value}\n")

    # =========================
    # FINE
    # =========================
    conn.send("\n")