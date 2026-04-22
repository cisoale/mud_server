from core.world import get_room
from core.combat_system import start_combat


def find_target(room, name):
    """
    Trova un mob nella stanza usando match parziale (case insensitive)
    """
    name = name.lower()

    matches = []

    for mob in room.mobs:
        if name in mob.get("name", "").lower():
            matches.append(mob)

    if not matches:
        return None

    # se più target → prende il primo (future: scelta numerica)
    return matches[0]


def execute(player, conn, args):

    # =========================
    # VALIDAZIONE
    # =========================
    if not args:
        conn.send("Attaccare cosa?\n")
        return

    if player.get("target"):
        conn.send("Sei già in combattimento!\n")
        return

    room = get_room(player.get("room"))

    if not room:
        conn.send("Errore: stanza non trovata.\n")
        return

    if not hasattr(room, "mobs"):
        conn.send("Errore: stanza corrotta.\n")
        return

    # =========================
    # TARGET
    # =========================
    target_name = " ".join(args)

    target = find_target(room, target_name)

    if not target:
        conn.send("Non trovi quel bersaglio.\n")
        return

    # evita attacco su mob già in combat con qualcun altro (opzionale)
    if target.get("target") and target["target"] != player:
        conn.send(f"{target['name']} è già impegnato in combattimento!\n")
        return

    # =========================
    # START COMBAT
    # =========================
    conn.send(f"Attacchi {target['name']}!\n")

    try:
        start_combat(player, target, conn)
    except Exception as e:
        print("[ERRORE ATTACK]", e)
        conn.send("Errore durante l'attacco.\n")