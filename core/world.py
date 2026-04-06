def spawn_player(player):
    race_data = get_race(player.race)
    start_zone = race_data["start_zone"]

    room = get_start_room(start_zone)
    player.room = room