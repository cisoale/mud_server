def execute(player, conn, args):

    if not args:
        conn.send("Usare cosa?\n")
        return

    inventory = player.get("inventory", [])
    search = " ".join(args).lower()

    for item in inventory:

        if not isinstance(item, dict):
            continue

        name = item.get("name", "").lower()

        if search in name:

            # =========================
            # NON USABILE
            # =========================
            consumable = item.get("consumable")

            if not consumable:
                conn.send("Non puoi usare questo oggetto.\n")
                return

            # =========================
            # APPLICA EFFETTI
            # =========================
            heal = consumable.get("heal", 0)
            mana = consumable.get("mana", 0)

            if heal > 0:
                player["hp"] = min(player.get("max_hp", 100), player.get("hp", 0) + heal)
                conn.send(f"Recuperi {heal} HP.\n")

            if mana > 0:
                player["mana"] = min(player.get("max_mana", 100), player.get("mana", 0) + mana)
                conn.send(f"Recuperi {mana} mana.\n")

            # =========================
            # CONSUMA OGGETTO
            # =========================
            qty = item.get("quantity", 1)

            if item.get("stackable") and qty > 1:
                item["quantity"] -= 1
            else:
                inventory.remove(item)

            conn.send(f"Usi {item.get('display_name', name)}.\n")

            return

    conn.send("Non hai quell'oggetto.\n")