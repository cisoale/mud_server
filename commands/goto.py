from core.world import get_room
from commands.look import execute as look


def execute(player, conn, args):

    # =========================
    # PERMESSI BUILDER
    # =========================
    if not player.get("builder"):
        conn.send("Non hai i permessi.\n")
        return

    # =========================
    # INPUT
    # =========================
    if not args:
        conn.send("Uso: goto <vnum>\n")
        return

    try:
        vnum = int(args[0])
    except:
        conn.send("Vnum non valido.\n")
        return

    new_room = get_room(vnum)

    if not new_room:
        conn.send("Room non trovata.\n")
        return

    # =========================
    # RIMUOVI DA VECCHIA ROOM
    # =========================
    old_room = get_room(player.get("room"))

    if old_room and hasattr(old_room, "players"):
        if player in old_room.players:
            old_room.players.remove(player)

    # =========================
    # AGGIUNGI ALLA NUOVA
    # =========================
    player["room"] = vnum

    if not hasattr(new_room, "players"):
        new_room.players = []

    new_room.players.append(player)

    conn.send(f"Ti sposti nella room {vnum}.\n")

    # =========================
    # AUTO LOOK
    # =========================
    look(player, conn, "look", [])