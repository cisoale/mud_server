import asyncio

from core.database import init_db
from core.command_handler import load_commands
from core.world_loader import load_rooms_from_files
from core.mob_loader import load_mobs
from core.item_loader import load_items
from core.world_loader import load_rooms_from_files
from core.server import MudServer
from core.mob_ai import mob_ai_loop


# init sistemi
init_db()
load_mobs()
load_items()
load_rooms_from_files()
load_commands()


async def main():

    server = MudServer(host="0.0.0.0", port=4000)

    asyncio.create_task(mob_ai_loop())  # 👈 AI ATTIVA

    await server.start()


if __name__ == "__main__":
    asyncio.run(main())