from core.data_loader import races
from core.world import get_room

def spawn_player(player):

    race = player.get("race", "umano")

    print("SPAWN DEBUG - RACE:", race)
    print("SPAWN DEBUG - RACES:", races)

    if race not in races:
        print("[ERRORE] razza non trovata:", race)
        player["room"] = 1001
        return

    start_room = races[race].get("start_room")

    print("SPAWN DEBUG - START ROOM:", start_room)

    # 🔥 CONTROLLO ESISTENZA
    room = get_room(start_room)

    if not room:
        print(f"[ERRORE] room {start_room} NON ESISTE")
        player["room"] = 1001
        return

    player["room"] = start_room