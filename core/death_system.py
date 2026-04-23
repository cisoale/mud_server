from core.gold_system import calculate_gold


def handle_death(attacker, target, room, broadcast):

    if not target or not room:
        return

    # =========================
    # 💰 GOLD
    # =========================
    gold = calculate_gold(target)

    if gold > 0 and attacker:
        attacker["gold"] = attacker.get("gold", 0) + gold
        broadcast(room, f"{attacker['name']} raccoglie {gold} monete.\n")

    # =========================
    # 💀 CORPO
    # =========================
    corpse = {
        "name": f"corpo di {target['name']}",
        "type": "corpse",
        "inventory": target.get("loot", [])
    }

    room.items.append(corpse)

    # =========================
    # 🧹 RIMOZIONE
    # =========================
    if target in room.mobs:
        room.mobs.remove(target)