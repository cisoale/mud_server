from core.world import get_room


def execute(player, conn, command, args):

    room = get_room(player.get("room"))

    if not room:
        conn.send("Stanza non trovata.\n")
        return

    # =========================
    # NOME + DESCRIZIONE
    # =========================
    conn.send(f"\n=== {room.name} ===\n")
    conn.send(f"{room.description}\n")

    # =========================
    # PLAYER
    # =========================
    others = []

    if hasattr(room, "players"):
        others = [p for p in room.players if p != player]

    if others:
        conn.send("\nGiocatori presenti:\n")
        for p in others:
            try:
                conn.send(f"- {p['name']}\n")
            except:
                pass

    # =========================
    # MOB
    # =========================
    if hasattr(room, "mobs") and room.mobs:
        conn.send("\nCreature presenti:\n")
        for i, mob in enumerate(room.mobs, 1):
            try:
                conn.send(f"{i}) {mob.get('name', 'mob')}\n")
            except:
                pass

    # =========================
    # OGGETTI
    # =========================
    if hasattr(room, "items") and room.items:
        conn.send("\nOggetti presenti:\n")
        for item in room.items:
            try:
                conn.send(f"- {item.get('name', 'oggetto')}\n")
            except:
                pass

    # =========================
    # USCITE
    # =========================
    if hasattr(room, "exits") and room.exits:
        conn.send("\nUscite:\n")
        conn.send(", ".join(room.exits.keys()) + "\n")

    conn.send("\n")