def execute(player, args, cmd=None):
    inv = player.get("inventory", [])

    if not inv:
        return "Il tuo inventario è vuoto."

    output = ["Inventario:"]

    for i, item in enumerate(inv):
        output.append(f"{i+1}. {item['name']}")

    return "\n".join(output)