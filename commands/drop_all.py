from core.world import get_room, broadcast_room


def execute(player, conn, args):

    room = get_room(player["room"])
    if not room:
        conn.send("Errore stanza.\n")
        return

    inventory = player.get("inventory", [])

    if not inventory:
        conn.send("Non hai nulla da lasciare.\n")
        return

    dropped = []

    # copiamo per sicurezza
    for item in list(inventory):
        room.items.append(item)
        dropped.append(item["name"])

    # svuota inventario
    player["inventory"] = []

    conn.send("Hai lasciato tutto a terra.\n")

    # messaggio agli altri
    broadcast_room(
        room,
        f"{player['name']} lascia cadere tutto a terra.\n",
        exclude=player
    )

    # debug opzionale
    print(f"[DROP ALL] {player['name']} -> {dropped}")