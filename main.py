import asyncio
from core.server import MudServer

if __name__ == "__main__":
    server = MudServer(host="0.0.0.0", port=4001)
    asyncio.run(server.start())