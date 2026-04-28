import asyncio

# =========================
# SERVER REALE
# =========================
from core.server import MudServer

# =========================
# COMMANDS
# =========================
from core.command_handler import load_commands

# =========================
# GAME SYSTEMS
# =========================
import core.world_loader as world_loader
import core.mob_loader as mob_loader
import core.item_loader as item_loader
import core.spawn_loader as spawn_loader

from core.mob_ai import mob_ai_loop
from core.combat_system import combat_tick


HOST = "0.0.0.0"
PORT = 4000


# =========================
# INIT GAME
# =========================
def initialize_game():

    print("\n=== AVVIO MUD SERVER ===\n")

    # -------------------------
    # MOBS (PRIMA!)
    # -------------------------
    print("[MOBS] Caricamento...")
    if hasattr(mob_loader, "load_mobs"):
        mob_loader.load_mobs()
    print("[MOBS] OK\n")

    # -------------------------
    # ITEMS
    # -------------------------
    print("[ITEMS] Caricamento...")
    if hasattr(item_loader, "load_items"):
        item_loader.load_items()
    print("[ITEMS] OK\n")

    # -------------------------
    # WORLD (DOPO mobs!)
    # -------------------------
    print("[WORLD] Caricamento...")

    if hasattr(world_loader, "load_rooms_from_files"):
        world_loader.load_rooms_from_files()

    print("[WORLD] OK\n")

    # -------------------------
    # NPC STATICI (ORA FUNZIONA)
    # -------------------------
    if hasattr(world_loader, "load_static_npcs"):
        world_loader.load_static_npcs()

    # -------------------------
    # SPAWN
    # -------------------------
    print("[SPAWN] Caricamento...")
    if hasattr(spawn_loader, "load_spawns"):
        spawn_loader.load_spawns()
    print("[SPAWN] OK\n")

    # -------------------------
    # COMMANDS
    # -------------------------
    load_commands()

    print("=== INIZIALIZZAZIONE COMPLETATA ===\n")

# =========================
# COMBAT LOOP
# =========================
async def combat_loop():

    while True:
        try:
            combat_tick()
        except Exception as e:
            print("[ERRORE COMBAT]", e)

        await asyncio.sleep(2)


# =========================
# MAIN
# =========================
async def main():

    initialize_game()

    # LOOP DI SISTEMA
    asyncio.create_task(mob_ai_loop())
    asyncio.create_task(combat_loop())

    # SERVER (TUO ORIGINALE)
    server = MudServer(HOST, PORT)
    await server.start()


# =========================
# START
# =========================
if __name__ == "__main__":
    asyncio.run(main())