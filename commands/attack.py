import asyncio
from core.combat_system import start_combat


def execute(player, conn, command, args):
    if not args:
        return "Attacca chi?"

    target_name = args[0].lower()
    room = player.get("room")

    if not room:
        return "Errore stanza."

    target = None

    for mob in room.mobs:
        if mob["name"].lower() == target_name:
            target = mob
            break

    if not target:
        return "Mob non trovato."

    # 🔥 PASSIAMO PLAYER (che ha writer)
    asyncio.create_task(start_combat(player, target))

    return f"Attacchi {target_name}!"