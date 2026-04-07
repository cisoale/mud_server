import asyncio
from core.combat_system import combat_loop


def execute(player, args, cmd=None):
    if not args:
        return "Attaccare cosa?"

    room = player.get("room")
    target_name = " ".join(args).lower()

    # 🔍 cerca mob
    for mob in room.mobs:
        if target_name in mob["name"].lower():

            # già in combat
            if player["combat"]["in_combat"]:
                return "Sei già in combattimento!"

            # imposta combat
            player["combat"]["target"] = mob
            player["combat"]["in_combat"] = True

            conn = player.get("conn")

            # 🔥 QUESTA DEVE STARE QUI DENTRO
            asyncio.create_task(combat_loop(player, conn))

            return f"Inizi a combattere contro {mob['name']}!"

    return "Nessun bersaglio trovato."