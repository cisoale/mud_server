from core.world import get_room
from core.simulation import global_world


# =========================
# WEATHER DESCRIPTIONS
# =========================

WEATHER_TEXT = {
    "clear": "Il cielo è limpido e tranquillo.",
    "rain": "La pioggia cade costantemente sulla regione.",
    "fog": "Una fitta nebbia avvolge l'area.",
    "storm": "Una violenta tempesta scuote la regione."
}


# =========================
# COMANDO LOOK
# =========================

def execute(player, conn, args):

    # sicurezza connessione
    if not conn:
        print("[LOOK ERROR] conn mancante execute")
        return

    # assegna connessione
    player["conn"] = conn

    render_room(player)


# =========================
# RENDER STANZA
# =========================

def render_room(player):

    conn = player.get("conn")

    if not conn:
        print("[LOOK ERROR] conn mancante render")
        return

    room = get_room(player.get("room"))

    if not room:
        conn.send("Errore: stanza non trovata.\n")
        return

    # =========================
    # NOME STANZA
    # =========================

    conn.send(
        f"\n"
        f"{getattr(room, 'name', 'Stanza sconosciuta')}\n"
    )

    # =========================
    # DESCRIZIONE
    # =========================

    desc = getattr(room, "description", "")

    if desc:
        conn.send(f"{desc}\n")

    # =========================
    # REGION + WEATHER
    # =========================

    region_id = getattr(
        room,
        "region_id",
        "starting_region"
    )

    region = global_world.region_system.get_region(
        region_id
    )

    if region:

        weather = getattr(
            region,
            "weather",
            "clear"
        )

        weather_text = WEATHER_TEXT.get(
            weather,
            "Il clima della regione è instabile."
        )

        conn.send(f"\n{weather_text}\n")

    # =========================
    # GIOCATORI
    # =========================

    players = getattr(room, "players", [])

    others = [
        p for p in players
        if p != player
    ]

    if others:

        conn.send("\nGiocatori presenti:\n")

        for p in others:

            name = p.get(
                "name",
                "giocatore"
            )

            conn.send(f" - {name}\n")

    # =========================
    # MOB
    # =========================

    mobs = getattr(room, "mobs", [])

    if mobs:

        conn.send("\nCreature presenti:\n")

        for mob in mobs:

            # sicurezza ECS / legacy
            if isinstance(mob, dict):

                name = mob.get(
                    "name",
                    "creatura"
                )

            elif hasattr(mob, "name"):

                name = mob.name

            else:

                name = "creatura sconosciuta"

            if not isinstance(name, str):
                name = "creatura sconosciuta"

            conn.send(f" - {name}\n")

    # =========================
    # OGGETTI A TERRA
    # =========================

    items = getattr(room, "items", [])

    if items:

        conn.send("\nA terra vedi:\n")

        counts = {}

        for item in items:

            # =========================
            # ITEM DICT
            # =========================

            if isinstance(item, dict):

                name = (
                    item.get("display_name")
                    or item.get("name", "oggetto")
                )

                qty = item.get(
                    "quantity",
                    1
                )

            # =========================
            # ITEM STRING LEGACY
            # =========================

            elif isinstance(item, str):

                name = item
                qty = 1

            # =========================
            # ECS OBJECT
            # =========================

            elif hasattr(item, "name"):

                name = item.name

                qty = getattr(
                    item,
                    "quantity",
                    1
                )

            # =========================
            # ITEM INVALIDO
            # =========================

            else:

                print(
                    f"[LOOK BUG] item sconosciuto: {item}"
                )

                continue

            # =========================
            # SICUREZZA
            # =========================

            if not isinstance(name, str):
                name = "oggetto corrotto"

            if not isinstance(qty, int):
                qty = 1

            if name not in counts:
                counts[name] = 0

            counts[name] += qty

        # =========================
        # RENDER ITEMS
        # =========================

        for name, qty in counts.items():

            if qty > 1:

                conn.send(
                    f" - {name} x{qty}\n"
                )

            else:

                conn.send(
                    f" - {name}\n"
                )

    # =========================
    # USCITE
    # =========================

    exits = getattr(room, "exits", {})

    if exits:

        exit_list = ", ".join(
            exits.keys()
        )

        conn.send(
            f"\nUscite: {exit_list}\n"
        )

    conn.send("\n")