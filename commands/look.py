from core.world import get_room


def render_room(player):

    room = get_room(player["room"])

    if not room:
        return "Stanza inesistente.\n"

    text = ""

    # =========================
    # NOME + DESCRIZIONE
    # =========================
    name = getattr(room, "name", "Unknown")
    desc = getattr(room, "description", "")

    text += f"\n[{name}]\n"
    text += f"{desc}\n"

    # =========================
    # USCITE
    # =========================
    exits = getattr(room, "exits", {})

    if exits:
        text += "\nUscite:\n"

        for direction, exit in exits.items():

            # sicurezza: exit deve essere dict
            if isinstance(exit, dict):

                if exit.get("secret"):
                    continue

                line = f"- {direction}"

                if exit.get("door"):
                    if exit.get("locked"):
                        line += " (bloccata)"
                    elif exit.get("closed"):
                        line += " (chiusa)"
                    else:
                        line += " (aperta)"

                text += line + "\n"

            else:
                # fallback vecchio sistema
                text += f"- {direction}\n"

    # =========================
    # MOB
    # =========================
    mobs = getattr(room, "mobs", [])

    if mobs:
        text += "\nCreature:\n"

        for mob in mobs:
            if isinstance(mob, dict):
                text += f"- {mob.get('name', 'mob')}\n"
            else:
                text += f"- {mob}\n"

    # =========================
    # OGGETTI
    # =========================
    items = getattr(room, "items", [])

    if items:
        text += "\nOggetti:\n"

        for item in items:
            if isinstance(item, dict):
                text += f"- {item.get('name', 'oggetto')}\n"
            else:
                text += f"- {item}\n"

    return text


# =========================
# COMANDO LOOK
# =========================
def execute(player, conn, command, args):

    text = render_room(player)

    try:
        conn.send(text)
    except:
        conn.send(text)