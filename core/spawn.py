from core.world import get_room


def spawn_player(player, races):

    # =========================
    # RAZZA → ROOM
    # =========================
    race = player.get("race")

    if not race or race not in races:
        print(f"[ERRORE] Razza non valida: {race}")
        start_room = 1001  # fallback sicuro
    else:
        start_room = races[race].get("start_room", 1001)

    player["room"] = start_room

    # =========================
    # RECUPERA ROOM
    # =========================
    room = get_room(start_room)

    if not room:
        print(f"[ERRORE] Room {start_room} non trovata")
        return

    # =========================
    # SICUREZZA STRUTTURA ROOM
    # =========================
    if not hasattr(room, "players"):
        room.players = []

    if not hasattr(room, "mobs"):
        room.mobs = []

    if not hasattr(room, "items"):
        room.items = []

    # =========================
    # EVITA DUPLICATI
    # =========================
    if player not in room.players:
        room.players.append(player)

    # =========================
    # DEBUG
    # =========================
    print(f"[SPAWN] {player['name']} -> Room {start_room}")

    # =========================
    # NOTIFICA ALTRI PLAYER
    # =========================
    for p in room.players:
        if p != player and isinstance(p, dict):
            conn = p.get("conn")
            if conn:
                try:
                    conn.send(f"{player['name']} è entrato nella stanza.\n")
                except:
                    pass