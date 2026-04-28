# =========================
# TRAVEL COMMAND (DICT SAFE)
# =========================

ALIASES = ["tp"]


def execute(player, conn, args):

    # =========================
    # INPUT
    # =========================
    if not args:
        conn.send("Uso: travel <vnum>\n")
        return

    try:
        vnum = int(args[0])
    except ValueError:
        conn.send("VNUM non valido.\n")
        return

    # =========================
    # CHECK ROOM
    # =========================
    try:
        from core.world import rooms
        target_room = rooms.get(vnum)
    except Exception:
        target_room = None

    if not target_room:
        conn.send("La stanza non esiste.\n")
        return

    # =========================
    # TELEPORT (FIX QUI)
    # =========================
    player["room"] = vnum

    conn.send(f"Ti sposti verso la stanza {vnum}\n")

    # =========================
    # AUTO LOOK
    # =========================
    try:
        from commands.look import execute as look
        look(player, conn, [])
    except Exception as e:
        print("[ERRORE LOOK]", e)