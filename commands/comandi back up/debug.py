from core.world import get_room


def execute(player, conn, args):

    room = get_room(player["room"])

    conn.send("\n--- DEBUG ROOM ITEMS ---\n")

    for item in room.items:
        conn.send(str(item) + "\n")

print("[DEBUG INVENTORY]", player.get("inventory"))