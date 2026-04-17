from core.world import get_room
from core.combat_system import start_combat


def execute(player, conn, command, args):

    # =========================
    # CONTROLLO INPUT
    # =========================
    if not args:
        conn.send("Attaccare chi?\n")
        return

    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    mobs = getattr(room, "mobs", [])

    # DEBUG
    conn.send(f"[DEBUG] Mob presenti: {len(mobs)}\n")

    if not mobs:
        conn.send("Non c'è nessun nemico qui.\n")
        return

    search = " ".join(args).lower()

    target = None

    # =========================
    # MATCH INTELLIGENTE
    # =========================
    for mob in mobs:

        if not isinstance(mob, dict):
            continue

        name = mob.get("name", "").lower()

        if (
            search in name
            or name in search
            or any(word in name for word in search.split())
        ):
            target = mob
            break

    # DEBUG TARGET
    conn.send(f"[DEBUG] Target trovato: {target}\n")

    if not target:
        conn.send("Non trovi quel nemico.\n")
        return

    # =========================
    # BLOCCA MULTI COMBAT
    # =========================
    if player.get("in_combat"):
        conn.send("Sei già in combattimento!\n")
        return

    # =========================
    # START COMBAT
    # =========================
    player["in_combat"] = True

    conn.send(f"Attacchi {target['name']}!\n")
    conn.send("[DEBUG] Avvio combat...\n")

    try:
        start_combat(player, target, conn)
    except Exception as e:
        conn.send(f"[ERRORE COMBAT] {e}\n")
        player["in_combat"] = False