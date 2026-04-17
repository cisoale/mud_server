from core.world import get_room
from core.mob_loader import get_mob_template, list_mobs
from core.item_loader import get_item_template
import copy


def execute(player, conn, command, args):

    # =========================
    # PERMESSI BUILDER
    # =========================
    if not player.get("builder"):
        conn.send("Non hai i permessi.\n")
        return

    if len(args) < 2:
        conn.send("Uso: spawn mob/item nome\n")
        return

    tipo = args[0].lower()
    name = " ".join(args[1:]).lower()

    room = get_room(player["room"])

    if not room:
        conn.send("Errore stanza.\n")
        return

    # =========================
    # SPAWN MOB
    # =========================
    if tipo == "mob":

        template = get_mob_template(name)

        if not template:
            conn.send("Mob non trovato.\n")
            conn.send(f"Disponibili: {', '.join(list_mobs())}\n")
            return

        mob = copy.deepcopy(template)

        # sicurezza
        mob["hp"] = mob.get("max_hp", 20)
        mob.setdefault("inventory", [])

        if not hasattr(room, "mobs"):
            room.mobs = []

        room.mobs.append(mob)

        conn.send(f"Hai spawnato {mob['name']}.\n")
        return

    # =========================
    # SPAWN ITEM
    # =========================
    elif tipo == "item":

        template = get_item_template(name)

        if not template:
            conn.send("Item non trovato.\n")
            return

        item = copy.deepcopy(template)

        if not hasattr(room, "items"):
            room.items = []

        room.items.append(item)

        conn.send(f"Hai spawnato {item['name']}.\n")
        return

    # =========================
    # ERRORE TIPO
    # =========================
    else:
        conn.send("Tipo non valido. Usa: mob o item\n")