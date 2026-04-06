from core.database import db

async def handle_login(conn):
    await conn.send("1) Login\n2) Registrati\n> ")
    choice = await conn.recv()

    if choice == "1":
        return await login(conn)
    else:
        return await register(conn)


async def register(conn):
    await conn.send("Nome: ")
    name = await conn.recv()

    await conn.send("Password: ")
    password = await conn.recv()

    await conn.send("Sesso: ")
    sex = await conn.recv()

    await conn.send("Razza: ")
    race = await conn.recv()

    await conn.send("Classe: ")
    cls = await conn.recv()

    player = db.create_player(name, password, sex, race, cls)
    return player