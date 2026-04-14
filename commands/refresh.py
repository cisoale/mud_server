from core.world_loader import load_rooms_from_files
from core.world import rooms
from core.server import connected_players

def get_all_players():
    return connected_players

def execute(player, args, cmd=None):
    if not player.get("builder"):
        return "Non hai i permessi."

    # 🧠 salva vecchie room
    old_rooms = rooms.copy()

    # 🔄 ricarica
    load_rooms_from_files()

    # 🔁 riallinea player alle nuove room
    for p in get_all_players():
        current = p.get("room")

        if current:
            new_room = rooms.get(current.vnum)

            if new_room:
                p["room"] = new_room

                # aggiungi alla nuova lista player
                if not hasattr(new_room, "players"):
                    new_room.players = []

                if p not in new_room.players:
                    new_room.players.append(p)

    return "Aree ricaricate con successo."