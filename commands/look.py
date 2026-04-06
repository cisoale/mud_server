def render_room(player):
    room = player.get("room")

    if not room:
        return "Sei nel vuoto."

    output = []

    # 🏠 nome + descrizione
    output.append(room.name)
    output.append(room.description)

    # 🚪 uscite
    exits = ", ".join(room.exits.keys())
    output.append(f"Uscite: {exits}")

    # 👥 player
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

    # 🎒 oggetti (anche corpse)
    if room.items:
        output.append("Oggetti:")
        for item in room.items:
            if item.get("type") == "corpse":
                output.append(f" - {item['name']} (corpse)")
            else:
                output.append(f" - {item['name']}")

    return "\n".join(output)


def execute(player, args, cmd=None):
    return render_room(player)