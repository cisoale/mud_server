from core.world import get_room

# 🧭 tutte le direzioni + abbreviazioni
DIRECTIONS = {
    "north": "north",
    "n": "north",

    "south": "south",
    "s": "south",

    "east": "east",
    "e": "east",

    "west": "west",
    "w": "west",

    "up": "up",
    "u": "up",

    "down": "down",
    "d": "down",
}


def execute(player, args, cmd=None):
    direction = DIRECTIONS.get(cmd)

    current_room = player.get("room")

    if direction not in current_room.exits:
        return f"Non puoi andare verso {direction}."

    new_room_vnum = current_room.exits[direction]
    new_room = get_room(new_room_vnum)

    # 🔴 rimuovi dalla stanza attuale
    if player in current_room.players:
        current_room.players.remove(player)

    # 🟢 aggiungi nuova stanza
    new_room.players.append(player)

    player["room"] = new_room

    # 👉 usa look automaticamente
    from commands.look import render_room
    return render_room(player)