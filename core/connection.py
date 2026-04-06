from systems.login.login import handle_login
from core.command_handler import handle_command
from core.spawn import spawn_player
from commands.look import render_room

class Connection:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def send(self, msg):
        self.writer.write((msg + "\n").encode())
        await self.writer.drain()

    async def recv(self):
        data = await self.reader.read(1024)
        if not data:
            return None
        return data.decode().strip()


async def handle_client(reader, writer):
    conn = Connection(reader, writer)

    try:
        # 🟢 Benvenuto
        await conn.send("Benvenuto nel MUD!")

        # 🔐 Login / Registrazione
        player = await handle_login(conn)
        
        room = spawn_player(player)

        if not room:
          await conn.send("Errore spawn. Contatta un admin.")
          writer.close()
          return

        await conn.send(render_room(player))
 
        if not player:
            await conn.send("Errore durante il login.")
            writer.close()
            return

        await conn.send(f"Benvenuto {player['name']}!")

        # 🔁 Game loop
        while True:
            await conn.send("> ")
            cmd = await conn.recv()

            # ❌ Connessione chiusa
            if cmd is None:
                break

            if cmd == "":
                continue

            # ⚙️ Gestione comando
            response = handle_command(player, cmd)

            # 🚪 Uscita
            if response == "quit":
                await conn.send("Arrivederci!")
                break

            await conn.send(response)

    except Exception as e:
        print(f"Errore connessione: {e}")

    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except:
            pass