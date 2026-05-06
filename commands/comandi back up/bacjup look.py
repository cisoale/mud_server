from core.world import get_room


# =========================
# COMANDO LOOK
# =========================
def execute(player, conn, args):
    # assicuriamo che il player abbia la connessione
    player["conn"] = conn
    render_room(player)


# =========================
# RENDER STANZA
# =========================
def render_room(player):

    conn = player.get("conn")
    if not conn:
        print("[LOOK ERROR] conn mancante")
        return

    room = get_room(player.get("room"))
    if not room:
        conn.send("Errore: stanza non trovata.\n")
        return

    # =========================
    # NOME + DESCRIZIONE
    # =========================
    conn.send(f"\n{getattr(room, 'name', 'Stanza sconosciuta')}\n")

    desc = getattr(room, "description", "")
    if desc:
        conn.send(f"{desc}\n")

    # =========================
    # GIOCATORI
    # =========================
    players = getattr(room, "players", [])
    others = [p for p in players if p != player]

    if others:
        conn.send("\nGiocatori presenti:\n")
        for p in others:
            name = p.get("name", "giocatore")
            conn.send(f" - {name}\n")

    # =========================
    # MOB
    # =========================
    mobs = getattr(room, "mobs", [])
    if mobs:
        conn.send("\nCreature presenti:\n")
        for mob in mobs:
            name = mob.get("name", "creatura")
            if not isinstance(name, str):
                name = "creatura sconosciuta"
            conn.send(f" - {name}\n")

    # =========================
    # OGGETTI A TERRA (FIX DEFINITIVO)
    # =========================
    items = getattr(room, "items", [])

    if items:
        conn.send("\nA terra vedi:\n")

        counts = {}

        for item in items:

            # sicurezza
            if not isinstance(item, dict):
                print(f"[LOOK BUG] item non valido: {item}")
                continue

            # nome leggibile
            name = item.get("display_name") or item.get("name", "oggetto")

            if not isinstance(name, str):
                name = "oggetto corrotto"

            qty = item.get("quantity", 1)
            if not isinstance(qty, int):
                qty = 1

            # 🔥 FIX: usare stringa come chiave
            if name not in counts:
                counts[name] = 0

            counts[name] += qty

        for name, qty in counts.items():
            if qty > 1:
                conn.send(f" - {name} x{qty}\n")
            else:
                conn.send(f" - {name}\n")

    # =========================
    # USCITE
    # =========================
    exits = getattr(room, "exits", {})

    if exits:
        exit_list = ", ".join(exits.keys())
        conn.send(f"\nUscite: {exit_list}\n")

    conn.send("\n")