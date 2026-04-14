from core.world import rooms


def execute(player, args, cmd=None):
    # 🔍 DEBUG (QUI DENTRO!)
    print("BUILDER:", player.get("builder"))

    # 🔒 permessi
    if not player.get("builder"):
        return "Non hai i permessi."

    if not args:
        return "Uso: goto <vnum>"

    try:
        vnum = int(args[0])
    except ValueError:
        return "VNUM non valido."

    room = rooms.get(vnum)

    if not room:
        return f"Room {vnum} non trovata."

    # 🚀 spostamento
    player["room"] = room

    from commands.look import render_room
    return render_room(player)


description = "Teletrasporta il player in una room (builder)."
usage = "goto <vnum>"