from core.world import rooms
from core.mob_loader import load_mobs
from core.item_loader import load_items
from core.world_loader import load_rooms_from_files


def execute(player, conn, command, args):

    # =========================
    # PERMESSI
    # =========================
    if not player.get("builder"):
        conn.send("Non hai i permessi.\n")
        return

    conn.send("🔄 Refresh del mondo in corso...\n")

    # =========================
    # SALVA POSIZIONE PLAYER
    # =========================
    current_room = player.get("room")

    # =========================
    # RESET WORLD
    # =========================
    rooms.clear()

    # =========================
    # RICARICA TUTTO
    # =========================
    load_mobs()
    load_items()
    load_rooms_from_files()

    # =========================
    # RIPOSIZIONA PLAYER
    # =========================
    from core.world import get_room

    new_room = get_room(current_room)

    if new_room:
        new_room.players.append(player)
        player["room"] = current_room
    else:
        conn.send("⚠️ Room non trovata, spawn default.\n")
        player["room"] = 1001
        get_room(1001).players.append(player)

    conn.send("✅ Mondo ricaricato con successo.\n")