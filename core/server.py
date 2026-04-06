import asyncio
from core.connection import handle_client

class MudServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def start(self):
        server = await asyncio.start_server(
            handle_client,
            self.host,
            self.port
        )

        print(f"MUD avviato su {self.host}:{self.port}")

        async with server:
            await server.serve_forever()