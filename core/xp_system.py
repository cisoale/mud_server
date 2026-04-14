async def send(player, msg):
    writer = player.get("writer")
    if writer:
        writer.write((msg + "\n").encode())
        await writer.drain()


async def add_xp(player, amount):
    player["xp"] += amount

    await send(player, f"+{amount} XP!")

    while True:
        needed = player["level"] * 100

        if player["xp"] < needed:
            break

        # 🔥 LEVEL UP
        player["xp"] -= needed
        player["level"] += 1

        # 📈 aumento stats
        player["max_hp"] += 10
        player["hp"] = player["max_hp"]

        await send(player, f"*** LEVEL UP! Ora sei livello {player['level']}! ***")