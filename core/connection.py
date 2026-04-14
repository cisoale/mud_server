import asyncio

from systems.login.login import handle_login
from core.command_handler import execute_command
from core.spawn import spawn_player
from commands.look import render_room


async def handle_client(reader, writer, server=None):

    addr = writer.get_extra_info('peername')
    print(f"[CONNESSIONE] {addr}")

    try:
        # =========================
        # LOGIN / REGISTRAZIONE
        # =========================
        player = await handle_login(reader, writer)

        if not player:
            writer.close()
            await writer.wait_closed()
            return

        # =========================
        # SPAWN PLAYER
        # =========================
        spawn_player(player)

        print(f"[SPAWN] {player['name']} -> Room {player['room']}")

        # mostra stanza iniziale
        writer.write(render_room(player).encode())
        await writer.drain()

        # =========================
        # LOOP COMANDI
        # =========================
        while True:

            writer.write(b"\n> ")
            await writer.drain()

            data = await reader.readline()

            if not data:
                break

            command_input = data.decode().strip()

            if not command_input:
                continue

            # =========================
            # PARSING COMANDO
            # =========================
            parts = command_input.split()

            cmd = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []

            print(f"[CMD] {player['name']}: {cmd} {args}")

            # =========================
            # ESECUZIONE COMANDO
            # =========================
            from core.connection_wrapper import Connection

            conn = Connection(writer)

            execute_command(cmd, player, conn, args)

    except Exception as e:
        print(f"[ERRORE CONNESSIONE] {e}")

    finally:
        print(f"[DISCONNESSO] {addr}")
        writer.close()
        await writer.wait_closed()