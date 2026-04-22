from core.effects_system import apply_effect

def execute(player, conn, args):

    if not args:
        conn.send("Usa: quaff <oggetto>\n")
        return

    for effect in item.get("effects", []):
      apply_effect(player, effect)
      conn.send(f"Effetto attivo: {effect['type']}\n")
    
    name = " ".join(args).lower()

    inventory = player.get("inventory", [])

    # 🔍 cerca item
    item = None
    for i in inventory:
        if i.get("name", "").lower() == name:
            item = i
            break

    if not item:
        conn.send("Non hai questo oggetto.\n")
        return

    # ❌ non è consumabile
    if item.get("type") != "consumable":
        conn.send("Non puoi usarlo.\n")
        return

    # 💊 effetti
    consumable = item.get("consumable", {})
    heal = consumable.get("heal", 0)
    mana = consumable.get("mana", 0)

    if heal == 0 and mana == 0:
        conn.send("Non succede nulla.\n")
        return

    # ❤️ HP
    if heal > 0:
        player["hp"] = player.get("hp", 0) + heal
        conn.send(f"Recuperi {heal} HP.\n")

    # 🔮 MANA
    if mana > 0:
        player["mana"] = player.get("mana", 0) + mana
        conn.send(f"Recuperi {mana} mana.\n")

    # 🗑️ rimuovi item
    inventory.remove(item)

    conn.send(f"Hai usato {item['name']}.\n")