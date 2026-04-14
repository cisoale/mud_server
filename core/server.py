import asyncio

from core.connection import handle_client

# 🌍 lista player connessi (globale)
connected_players = []


def get_all_players():
    return connected_players


class MudServer:
    def __init__(self, host="0.0.0.0", port=4000):
        self.host = host
        self.port = port

    async def start(self):
        server = await asyncio.start_server(
            self.client_connected,
            self.host,
            self.port
        )

        print(f"MUD avviato su {self.host}:{self.port}")

        async with server:
            await server.serve_forever()

    async def client_connected(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"[CONNESSIONE] {addr}")

        # 👤 crea player vuoto
        player = {
            "name": None,
            "room": None,
            "inventory": [],
            "equipment": {},
            "builder": False
        }

        # ➕ aggiungi alla lista globale
        connected_players.append(player)

        try:
            # 🚀 passa tutto al gestore principale
            await handle_client(reader, writer, player)

        except Exception as e:
            print(f"[ERRORE CONNESSIONE] {e}")

        finally:
            print(f"[DISCONNESSO] {addr}")

            # ➖ rimuovi player dalla room
            room = player.get("room")
            if room and hasattr(room, "players"):
                if player in room.players:
                    room.players.remove(player)

            # ➖ rimuovi dalla lista globale
            if player in connected_players:
                connected_players.remove(player)

            writer.close()
            await writer.wait_closed()