from core.data_loader import races
from core.world import get_room


def spawn_player(player):
    from core.world import get_room

    race_data = races.get(player["race"])
    start_room = get_room(race_data["start_room"])

    player["room"] = start_room

    # 👉 aggiungi player alla stanza
    start_room.players.append(player)

    return start_room