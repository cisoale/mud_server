def render_room(player):
    room = player.get("room")

    if not room:
        return "Sei nel vuoto."

    output = []

    # 🏠 nome + descrizione
    output.append(f"{room.name}")
    output.append(f"{room.description}")

    # 🚪 uscite
    exits = ", ".join(room.exits.keys())
    output.append(f"Uscite: {exits}")

    # 👥 altri player
    others = [p["name"] for p in room.players if p != player]
    if others:
        output.append("Giocatori presenti:")
        for p in others:
            output.append(f" - {p}")

    # 👹 mob
    if room.mobs:
        output.append("Creature:")
        for mob in room.mobs:
            output.append(f" - {mob['name']}")

    # 🎒 oggetti
    if room.items:
        output.append("Oggetti:")
        for item in room.items:
            output.append(f" - {item['name']}")

    return "\n".join(output)


def execute(player, args, cmd=None):
    return render_room(player)