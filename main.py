import asyncio

from core.database import init_db
from core.command_handler import load_commands
from core.world_loader import load_rooms_from_files
from core.mob_loader import load_mobs
from core.world import load_world
from core.server import MudServer

# init sistemi
init_db()
load_mobs()
load_rooms_from_files()
load_commands()
load_world()

if __name__ == "__main__":
    server = MudServer(host="0.0.0.0", port=4000)
    asyncio.run(server.start())