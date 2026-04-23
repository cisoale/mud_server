from core.world import get_room


def execute(player, conn, args):

    if not args or not args[0].isdigit():
        conn.send("Uso: dropgold <quantità>\n")
        return

    amount = int(args[0])

    if amount <= 0:
        return

    if player.get("gold", 0) < amount:
        conn.send("Non hai abbastanza oro.\n")
        return

    room = get_room(player["room"])

    player["gold"] -= amount

    pile = {
        "name": f"{amount} monete",
        "type": "gold",
        "amount": amount
    }

    room.items.append(pile)

    conn.send(f"Hai lasciato {amount} monete.\n")