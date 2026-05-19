import os

from config import ROOMS_DIR
from services.file_service import load_json, save_json



def get_rooms():

    rooms = []

    for root, dirs, files in os.walk(ROOMS_DIR):

        for file in files:

            if not file.endswith('.json'):
                continue

            path = os.path.join(root, file)

            data = load_json(path)

            if data:
                rooms.append(data)

    rooms.sort(
        key=lambda r: r.get('vnum', 0)
    )

    return rooms



def save_room(room):

    vnum = room.get('vnum')

    if not vnum:
        return False

    path = os.path.join(
        ROOMS_DIR,
        f'{vnum}.json'
    )

    save_json(path, room)

    return True