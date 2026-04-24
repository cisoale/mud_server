from core.gold_system import calculate_gold


def handle_death(attacker, target, room, broadcast):
    """
    Gestisce morte di un'entità:
    - assegna gold
    - crea corpse
    - NON rimuove il mob (lo fa combat_system)
    """

    if not target or not room:
        print("[DEATH ERROR] target o room non validi")
        return

    # =========================
    # 💰 GOLD
    # =========================
    gold = calculate_gold(target)

    if gold > 0 and attacker:
        attacker["gold"] = attacker.get("gold", 0) + gold

        broadcast(
            room,
            f"{attacker['name']} raccoglie {gold} monete.\n"
        )

        print(f"[GOLD] {attacker['name']} +{gold} (tot={attacker['gold']})")

    # =========================
    # 💀 CORPO
    # =========================
    corpse = {
        "name": f"corpo di {target['name']}",
        "type": "corpse",
        "inventory": [],  # 🔥 NON usare target["loot"]
    }

    room.items.append(corpse)

    print(f"[DEATH] Creato corpse per {target['name']}")