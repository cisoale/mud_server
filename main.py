import asyncio
from core.server import MudServer
from core.command_handler import load_commands

if __name__ == "__main__":
    load_commands()
    
    server = MudServer(host="0.0.0.0", port=4001)
    asyncio.run(server.start())
    