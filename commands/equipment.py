SLOTS = [
    "testa",
    "torso",
    "gambe",
    "piedi",
    "mani",
    "arma",
    "secondaria",
    "anello1",
    "anello2",
    "collo"
]


def execute(player, conn, args):

    equip = player.get("equipment", {})

    conn.send("\n=== EQUIPAGGIAMENTO ===\n")

    for slot in SLOTS:

        item = equip.get(slot)

        if item:
            conn.send(f"{slot.capitalize()}: {item.get('name')}\n")
        else:
            conn.send(f"{slot.capitalize()}: ---\n")