from systems.login.login import handle_login
from core.command_handler import execute_command


# =========================
# INPUT SICURO
# =========================
async def read_input(conn):

    while True:
        data = await conn.reader.readline()

        if not data:
            return None

        text = data.decode().strip()

        if text != "":
            return text


# =========================
# GESTIONE CLIENT
# =========================
async def handle_client(reader, writer, server):

    addr = writer.get_extra_info('peername')
    print(f"[CONNESSIONE] {addr}")

    conn = Connection(reader, writer)
    player = None

    try:
        # =========================
        # LOGIN
        # =========================
        player = await handle_login(conn)

        if not player:
            writer.close()
            await writer.wait_closed()
            return

        player["conn"] = conn

        # =========================
        # LOOP COMANDI
        # =========================
        while True:

            conn.send("\n> ")

            # 🔥 QUI DEFINISCI input_text
            input_text = await read_input(conn)

            if not input_text:
                break

            execute_command(player, conn, input_text)

    except Exception as e:
        print(f"[ERRORE CONNESSIONE] {e}")

    finally:
        print(f"[DISCONNESSO] {addr}")

        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass


# =========================
# WRAPPER CONNESSIONE
# =========================
class Connection:

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    def send(self, text):
        try:
            self.writer.write((text + "\n").encode())
        except:
            pass