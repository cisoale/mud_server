from core.mob_loader import mobs_data
from core.mob_factory import create_mob
import json
import os


def execute(player, args, cmd=None):
    if len(args) < 2:
        return "Uso: spawn <mob/item> <nome>"

    type_ = args[0].lower()
    name = " ".join(args[1:]).lower()

    room = player.get("room")

    # =========================
    # 👹 SPAWN MOB
    # =========================
    if type_ == "mob":
        mob_data = mobs_data.get(name)

        if not mob_data:
            return f"Mob '{name}' non trovato."

        mob = create_mob(
            mob_data["name"],
            mob_data.get("description", ""),
            mob_data.get("hp", 10),
            mob_data.get("inventory", []),
            mob_data.get("xp", 10)
        )

        room.mobs.append(mob)
        return f"Mob '{name}' spawnato."

    # =========================
    # 🎒 SPAWN ITEM
    # =========================
    elif type_ == "item":
        path = os.path.join("data/items", f"{name}.json")

        if not os.path.exists(path):
            return f"Item '{name}' non trovato."
        
        if not player.get("builder"):
            return "Non hai i permessi."

        with open(path, encoding="utf-8") as f:
            item = json.load(f)

        room.items.append(item)
        return f"Item '{name}' spawnato."

    return "Tipo non valido (mob/item)."

description = "Spawna mob o item nella stanza (builder)."
usage = "spawn <mob/item> <nome>"