from core.world import get_room
from core.data_loader import races

def spawn_player(player):

    race = player.get("race") or "umano"
    start_room_vnum = races.get(race, {}).get("start_room", 1001)

    room = get_room(start_room_vnum)

    if not room:
        print(f"[ERRORE] Room non trovata: {start_room_vnum}")
        return None

    # 🔥 SET CORRETTO
    player["room"] = room.vnum

    # 🔥 AGGIUNGI ALLA ROOM
    if player not in room.players:
        room.players.append(player)
   
    print(f"[SPAWN] {player['name']} -> Room {room.vnum}")

    return room