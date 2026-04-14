from core.database import create_player, get_player


async def handle_login(reader, writer):

    writer.write(b"\n1) Login\n2) Registrazione\n> ")
    await writer.drain()

    choice = (await reader.readline()).decode().strip()

    # =========================
    # LOGIN
    # =========================
    if choice == "1":

        writer.write(b"Nome: ")
        await writer.drain()
        name = (await reader.readline()).decode().strip()

        writer.write(b"Password: ")
        await writer.drain()
        password = (await reader.readline()).decode().strip()

        player = get_player(name)

        if not player:
            writer.write(b"Utente non trovato.\n")
            await writer.drain()
            return None

        if player["password"] != password:
            writer.write(b"Password errata.\n")
            await writer.drain()
            return None

        writer.write(b"Login effettuato!\n")
        await writer.drain()

        return player

    # =========================
    # REGISTRAZIONE
    # =========================
    elif choice == "2":

        writer.write(b"Nome: ")
        await writer.drain()
        name = (await reader.readline()).decode().strip()

        if get_player(name):
            writer.write(b"Nome gia' esistente.\n")
            await writer.drain()
            return None

        writer.write(b"Password: ")
        await writer.drain()
        password = (await reader.readline()).decode().strip()

        create_player(name, password)

        writer.write(b"Registrazione completata!\n")
        await writer.drain()

        return get_player(name)

    else:
        writer.write(b"Scelta non valida.\n")
        await writer.drain()
        return None