from core.data_loader import races, classes
from core.database import create_player, get_player


# 🧠 inizializzazione stato player
def init_player_state(player):
    # 🎒 inventario
    player.setdefault("inventory", [])

    # 🛡️ equip
    player.setdefault("equipment", {
        "head": None,
        "chest": None,
        "legs": None,
        "feet": None,
        "hands": None,
        "weapon": None,
        "shield": None,
        "ring": None,
        "amulet": None
    })

    # ❤️ hp base
    player.setdefault("hp", 20)
    player.setdefault("max_hp", 20)
    player.setdefault("level", 1)
    player.setdefault("xp", 0)
    player.setdefault("xp_to_next", 100)

    # ⚔️ stato combat
    player.setdefault("combat", {
    "target": None,
    "in_combat": False
})

    player.setdefault("hp", 20)
    player.setdefault("max_hp", 20)

    player.setdefault("level", 1)
    player.setdefault("xp", 0)
    player.setdefault("xp_to_next", 100)

    return player


# 🔁 MENU LOGIN
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

    if player:
        player = init_player_state(player)
  
    if player and player["password"] == password:
        player = init_player_state(player)

        await conn.send("Login effettuato!")
        return player
    
    if player["name"] == "wiz":
       player["builder"] = True

    await conn.send("Credenziali errate.")
    return None


# 🔁 FUNZIONE SCELTE
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

        # controlla se esiste già
        if get_player(name):
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

    # 🔥 inizializza inventario + equip
    player = init_player_state(player)

    # 💾 salva su database
    create_player(player)

    await conn.send("Registrazione completata!")

    return player