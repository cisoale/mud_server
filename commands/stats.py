from core.inventory import get_total_weight


def execute(player, conn, command, args):

    if not player:
        conn.send("Errore player.\n")
        return

    name = player.get("name", "Unknown")
    level = player.get("level", 1)
    xp = player.get("xp", 0)

    hp = player.get("hp", 100)
    max_hp = player.get("max_hp", 100)

    # =========================
    # STATISTICHE BASE
    # =========================
    strength = player.get("str", 10)
    dexterity = player.get("dex", 10)
    intelligence = player.get("int", 10)

    # =========================
    # INVENTARIO
    # =========================
    current_weight = get_total_weight(player)
    max_weight = player.get("max_weight", 50)

    # =========================
    # EQUIP
    # =========================
    equipment = player.get("equipment", {})

    # =========================
    # OUTPUT
    # =========================
    text = f"\n=== {name} ===\n"

    text += f"Livello: {level}  XP: {xp}\n"
    text += f"HP: {hp}/{max_hp}\n\n"

    text += "Statistiche:\n"
    text += f" STR: {strength}\n"
    text += f" DEX: {dexterity}\n"
    text += f" INT: {intelligence}\n\n"

    text += f"Peso: {current_weight}/{max_weight}\n\n"

    # =========================
    # EQUIP VISIVO
    # =========================
    text += "Equipaggiamento:\n"

    if not equipment:
        text += " Nessuno\n"
    else:
        for slot, item in equipment.items():

            if isinstance(item, dict):
                name = item.get("name", "oggetto")
            else:
                name = str(item)

            text += f" {slot}: {name}\n"

    conn.send(text)