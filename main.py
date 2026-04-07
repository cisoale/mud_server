import asyncio
from core.world_loader import load_rooms_from_files
from core.mob_loader import load_mobs

load_mobs()
load_rooms_from_files()
from core.server import MudServer
from core.command_handler import load_commands
from core.world import load_world
from core.database import init_db
init_db()

if __name__ == "__main__":
    # 🔧 carica sistemi
    load_commands()
    load_world()

    # 🚀 avvia server
    server = MudServer(host="0.0.0.0", port=4000)
    asyncio.run(server.start())