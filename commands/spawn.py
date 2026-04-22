from core.mob_loader import create_mob
from core.item_loader import create_item
from core.world import get_room


def parse_target(target):
    """
    Converte automaticamente:
    - numeri → vnum (string)
    - testo → nome lowercase
    """
    if target.isdigit():
        return target  # vnum già ok
    return target.lower()


def execute(player, conn, args):

    if not args:
        conn.send("Uso: spawn mob|item <nome/vnum> [quantità]\n")
        return

    if not player.get("is_builder"):
        conn.send("Non hai i permessi.\n")
        return

    tipo = args[0].lower()

    if len(args) < 2:
        conn.send("Specifica cosa spawnare.\n")
        return

    target_raw = args[1]
    target = parse_target(target_raw)

    quantità = 1
    if len(args) > 2 and args[2].isdigit():
        quantità = int(args[2])

    room = get_room(player.get("room"))

    if not room:
        conn.send("Errore stanza.\n")
        return

    # =========================
    # MOB
    # =========================
    if tipo == "mob":

        spawned = 0

        for _ in range(quantità):
            mob = create_mob(target)

            if not mob:
                conn.send(f"Mob non trovato: {target_raw}\n")
                return

            room.mobs.append(mob)
            spawned += 1

        conn.send(f"Spawnati {spawned} mob: {target_raw}\n")
        return

    # =========================
    # ITEM
    # =========================
    elif tipo == "item":

        spawned = 0

        for _ in range(quantità):
            item = create_item(target)

            if not item:
                conn.send(f"Item non trovato: {target_raw}\n")
                return

            room.items.append(item)
            spawned += 1

        conn.send(f"Spawnati {spawned} item: {target_raw}\n")
        return

    else:
        conn.send("Tipo non valido (mob/item)\n")