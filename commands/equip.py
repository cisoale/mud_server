def execute(player, conn, args):

    if not args:
        conn.send("Equip cosa?\n")
        return

    search = " ".join(args).lower()

    inventory = player.get("inventory", [])

    if not inventory:
        conn.send("Non hai oggetti.\n")
        return

    target = None

    # =========================
    # 🔍 MATCH INTELLIGENTE
    # =========================
    for item in inventory:

        if isinstance(item, dict):
            name = item.get("name", "").lower()
        else:
            name = str(item).lower()

        if (
            search in name
            or name in search
            or any(word in name for word in search.split())
        ):
            target = item
            break

    if not target:
        conn.send("Non ce l'hai.\n")
        return

    if not isinstance(target, dict):
        conn.send("Non puoi equipaggiare questo oggetto.\n")
        return

    # =========================
    # SLOT
    # =========================
    slot = target.get("slot")

    if not slot:
        conn.send("Non puoi equipaggiare questo oggetto.\n")
        return

    equipment = player.setdefault("equipment", {})

    # =========================
    # SE SLOT OCCUPATO → SWAP
    # =========================
    if slot in equipment:

        old_item = equipment[slot]

        inventory.append(old_item)

        old_name = old_item.get("name", "oggetto")

        conn.send(f"Togli {old_name}.\n")

    # =========================
    # EQUIP
    # =========================
    equipment[slot] = target
    inventory.remove(target)

    name = target.get("name", "oggetto")

    conn.send(f"Equipaggi {name} nello slot {slot}.\n")