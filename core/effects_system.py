import time


def apply_effects(player):

    effects = {}

    # da equip
    for item in player.get("equipment", {}).values():
        for k, v in item.get("effects", {}).items():
            effects[k] = effects.get(k, 0) + v

    # applica
    if effects.get("regen_hp"):
        player["hp"] += effects["regen_hp"]

    if effects.get("regen_mana"):
        player["mana"] += effects["regen_mana"]
        
def process_effects(target, conn=None):

    if "effects" not in target:
        return

    now = time.time()
    to_remove = []

    for effect in target["effects"]:

        # tick
        if now - effect["last_tick"] >= effect.get("tick", 1):

            effect["last_tick"] = now

            if effect["type"] == "poison":
                target["hp"] -= effect["value"]
                if conn:
                    conn.send(f"💀 Il veleno ti infligge {effect['value']} danni!\n")

            elif effect["type"] == "regen":
                target["hp"] += effect["value"]
                if conn:
                    conn.send(f"✨ Rigeneri {effect['value']} HP.\n")

            elif effect["type"] == "stun":
                if conn:
                    conn.send("⚡ Sei stordito!\n")

        # durata
        effect["duration"] -= 1
        if effect["duration"] <= 0:
            to_remove.append(effect)

    for e in to_remove:
        target["effects"].remove(e)
        if conn:
            conn.send(f"L'effetto {e['type']} termina.\n")