from core.data_loader import races, classes
from core.database import create_player, get_player

# ⚠️ temporaneo (RAM) → poi passeremo a DB
players = {}


async def handle_login(conn):
    while True:
        await conn.send("1) Login")
        await conn.send("2) Registrati")
        await conn.send("> ")

        choice = await conn.recv()

        if choice == "1":
            player = await login(conn)
            if player:
                return player

        elif choice == "2":
            return await register(conn)

        else:
            await conn.send("Scelta non valida.")


# 🔐 LOGIN
async def login(conn):
    await conn.send("=== Login ===")

    await conn.send("Nome: ")
    name = await conn.recv()

    await conn.send("Password: ")
    password = await conn.recv()

    player = get_player(name)

    if player and player["password"] == password:
        await conn.send("Login effettuato!")
        return player

    await conn.send("Credenziali errate.")
    return None

# 🔁 FUNZIONE GENERICA PER SCELTE
async def ask_choice(conn, prompt, options):
    options_list = list(options.keys())

    while True:
        await conn.send(f"{prompt}: {', '.join(options_list)}")
        choice = await conn.recv()

        if not choice:
            continue

        choice = choice.lower()

        if choice in options_list:
            return choice

        await conn.send("Scelta non valida, riprova.")


# 🆕 REGISTRAZIONE
async def register(conn):
    await conn.send("=== Registrazione ===")

    # Nome
    while True:
        await conn.send("Nome: ")
        name = await conn.recv()

        if not name:
            await conn.send("Nome non valido.")
            continue

        if name in players:
            await conn.send("Nome già esistente.")
            continue

        break

    # Password
    while True:
        await conn.send("Password: ")
        password = await conn.recv()

        if password:
            break

        await conn.send("Password non valida.")

    # Sesso
    sex_options = {
        "m": "Maschio",
        "f": "Femmina"
    }
    sex = await ask_choice(conn, "Sesso (m/f)", sex_options)

    # Razza
    race = await ask_choice(conn, "Razza", races)

    # Classe
    cls = await ask_choice(conn, "Classe", classes)

    # Creazione player
    player = {
        "name": name,
        "password": password,
        "sex": sex,
        "race": race,
        "class": cls
    }

    create_player(player)

    await conn.send("Registrazione completata!")

    return player