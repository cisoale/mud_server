import json
import time
import random

from core.world import get_room
from core.mob_loader import create_mob

SPAWNS = []


# =========================
# SPAWN POINT
# =========================
class SpawnPoint:
    def __init__(self, data):
        self.room = data["room"]
        self.mob = data["mob"]

        self.max_alive = data.get("max_alive", 1)
        self.respawn = data.get("respawn", 30)

        self.last_spawn = 0

    # =========================
    # COUNT MOB PER TIPO
    # =========================
    def alive_count(self):
        room = get_room(self.room)
        if not room:
            return 0

        # conta solo i mob di questo tipo
        return sum(1 for m in room.mobs if m["name"] == self.mob)

    # =========================
    # SPAWN LOGIC
    # =========================
    def try_spawn(self):
        room = get_room(self.room)
        if not room:
            return

        # limite per tipo
        alive = self.alive_count()
        if alive >= self.max_alive:
            return

        # tempo attuale
        now = time.time()

        # variazione naturale spawn
        delay = self.respawn + random.randint(-3, 3)

        if now - self.last_spawn < delay:
            return

        # crea mob
        mob = create_mob(self.mob)
        if not mob:
            print(f"[SPAWN] Mob non trovato: {self.mob}")
            return

        # assegna room
        room.mobs.append(mob)
        mob["room"] = room.vnum

        self.last_spawn = now

        print(f"[SPAWN] {mob['name']} in room {room.vnum}")


# =========================
# LOAD SPAWNS
# =========================
def load_spawns():
    global SPAWNS
    SPAWNS = []

    try:
        with open("data/spawns.json", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("[SPAWN] Nessun file spawns.json trovato - spawn disattivato")
        return
    except Exception as e:
        print(f"[SPAWN] Errore caricamento: {e}")
        return

    for entry in data:
        try:
            SPAWNS.append(SpawnPoint(entry))
        except Exception as e:
            print(f"[SPAWN] Errore entry: {entry} -> {e}")

    print(f"[SPAWN] Caricati {len(SPAWNS)} spawn point")


# =========================
# LOOP SPAWN
# =========================
def spawn_loop():
    for sp in SPAWNS:
        try:
            sp.try_spawn()
        except Exception as e:
            print(f"[ERRORE SPAWN] {e}")