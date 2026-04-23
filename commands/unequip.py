from core.equipment import unequip_item


def execute(player, conn, args):

    if not args:
        conn.send("Specifica lo slot.\n")
        return

    slot = args[0]

    msg = unequip_item(player, slot)
    conn.send(msg + "\n")