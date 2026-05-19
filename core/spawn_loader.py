import json
import time
import random

from core.world import get_room

# TEMPLATE LOADER
from core.mob_loader import get_mob

# ECS RUNTIME FACTORY
from core.mob_factory import create_mob

SPAWNS = []


# =========================
# SPAWN POINT
# =========================
class SpawnPoint:

    def __init__(self, data):

        self.room = data["room"]

        self.mob = data["mob"]

        self.max_alive = data.get(
            "max_alive",
            1
        )

        self.respawn = data.get(
            "respawn",
            30
        )

        self.last_spawn = 0

    # =========================
    # COUNT MOBS
    # =========================
    def alive_count(self):

        room = get_room(self.room)

        if not room:
            return 0

        return sum(
            1
            for m in room.mobs
            if m["name"] == self.mob
        )

    # =========================
    # SPAWN LOGIC
    # =========================
    def try_spawn(self):

        room = get_room(self.room)

        if not room:
            return

        # limite spawn
        alive = self.alive_count()

        if alive >= self.max_alive:
            return

        # tempo
        now = time.time()

        # variazione naturale
        delay = self.respawn + random.randint(-3, 3)

        if now - self.last_spawn < delay:
            return

        # =========================
        # TEMPLATE
        # =========================

        template = get_mob(self.mob)

        if not template:

            print(
                f"[SPAWN] Mob non trovato: "
                f"{self.mob}"
            )

            return

        # =========================
        # ECS RUNTIME MOB
        # =========================

        mob = create_mob(template)

        if not mob:
            return

        # assegna room
        room.mobs.append(mob)

        mob["room"] = room.vnum

        # aggiorna PositionComponent
        position = mob["components"].get(
            "PositionComponent"
        )

        if position:
            position.room_id = room.vnum

        self.last_spawn = now

        # DEBUG ECS
        print(
            f"[ECS] Spawnato mob: "
            f"{mob['name']} -> "
            f"{list(mob['components'].keys())}"
        )

        print(
            f"[SPAWN] {mob['name']} "
            f"in room {room.vnum}"
        )


# =========================
# LOAD SPAWNS
# =========================
def load_spawns():

    global SPAWNS

    SPAWNS = []

    try:

        with open(
            "data/spawns.json",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

    except FileNotFoundError:

        print(
            "[SPAWN] Nessun "
            "spawns.json trovato"
        )

        return

    except Exception as e:

        print(
            f"[SPAWN] Errore caricamento: {e}"
        )

        return

    for entry in data:

        try:

            SPAWNS.append(
                SpawnPoint(entry)
            )

        except Exception as e:

            print(
                f"[SPAWN] Errore entry: "
                f"{entry} -> {e}"
            )

    print(
        f"[SPAWN] Caricati "
        f"{len(SPAWNS)} spawn point"
    )


# =========================
# SPAWN LOOP
# =========================
def spawn_loop():

    for sp in SPAWNS:

        try:

            sp.try_spawn()

        except Exception as e:

            print(
                f"[ERRORE SPAWN] {e}"
            )