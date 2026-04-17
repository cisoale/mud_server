import json
from core.database import get_player, create_player
from core.spawn import spawn_player
from core.data_loader import races, classes


# =========================
# SAFE JSON LOAD
# =========================
def safe_load(data, default):

    if isinstance(data, str):
        try:
            return json.loads(data)
        except:
            return default

    if isinstance(data, (list, dict)):
        return data

    return default


# =========================
# MENU LOGIN
# =========================
async def handle_login(conn):

    conn.send("Benvenuto nel MUD!\n")
    conn.send("1) Login\n2) Registrati\n> ")

    choice = (await conn.reader.readline()).decode().strip()

    if choice == "2":
        return await register(conn)
    else:
        return await login(conn)


# =========================
# LOGIN
# =========================
async def login(conn):

    conn.send("Nome: ")
    name = (await conn.reader.readline()).decode().strip()

    conn.send("Password: ")
    password = (await conn.reader.readline()).decode().strip()

    player_data = get_player(name)

    if not player_data:
        conn.send("Player non trovato.\n")
        return None

    if player_data["password"] != password:
        conn.send("Password errata.\n")
        return None

    # =========================
    # COSTRUZIONE PLAYER
    # =========================
    player = {
        "name": name,
        "race": player_data.get("race") or "umano",

        "hp": player_data.get("hp", 100),
        "max_hp": player_data.get("max_hp", 100),

        "level": player_data.get("level", 1),
        "xp": player_data.get("xp", 0),

        "room": player_data.get("room", 1001),

        "inventory": safe_load(player_data.get("inventory"), []),
        "equipment": safe_load(player_data.get("equipment"), {}),

        "builder": player_data.get("builder", 0),

        "str": player_data.get("str", 10),
        "dex": player_data.get("dex", 10),

        "in_combat": False
    }

    # =========================
    # SPAWN
    # =========================
    spawn_player(player, races)

    conn.send(f"\nLogin effettuato! Benvenuto {name}.\n")

    return player


# =========================
# REGISTRAZIONE
# =========================
async def register(conn):

    conn.send("Nome: ")
    name = (await conn.reader.readline()).decode().strip()

    conn.send("Password: ")
    password = (await conn.reader.readline()).decode().strip()

    # =========================
    # RAZZE
    # =========================
    conn.send("\nRazze disponibili:\n")
    for r in races:
        conn.send(f"- {r}\n")

    conn.send("Scegli razza: ")
    race = (await conn.reader.readline()).decode().strip().lower()

    if race not in races:
        conn.send("Razza non valida.\n")
        return None

    # =========================
    # CLASSI
    # =========================
    conn.send("\nClassi disponibili:\n")
    for c in classes:
        conn.send(f"- {c}\n")

    conn.send("Scegli classe: ")
    classe = (await conn.reader.readline()).decode().strip().lower()

    if classe not in classes:
        conn.send("Classe non valida.\n")
        return None

    # =========================
    # CREA PLAYER
    # =========================
    create_player(name, password, race, classe)

    conn.send("\nRegistrazione completata! Ora fai login.\n")

    return None