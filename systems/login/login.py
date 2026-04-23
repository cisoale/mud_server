from core.database import get_player, create_player
from core.world import get_room
from core.spawn import spawn_player
from core.skill_system import unlock_skills  # 🔥 FIX IMPORT


# =========================
# INPUT
# =========================
async def ask(conn, text):
    conn.send(text)
    data = await conn.reader.readline()
    return data.decode().strip()


# =========================
# LOGIN
# =========================
async def handle_login(conn):

    conn.send("\n=== BENVENUTO ===\n")
    conn.send("1) Login\n")
    conn.send("2) Registrati\n> ")

    choice = (await conn.reader.readline()).decode().strip()

    # =========================
    # LOGIN
    # =========================
    if choice == "1":

        name = await ask(conn, "Nome: ")
        password = await ask(conn, "Password: ")

        player = get_player(name)

        # 🔥 FIX: controlla prima che esista
        if not player:
            conn.send("Player non trovato.\n")
            return None

        # 🔥 BUILDER SAFE
        if player["name"].lower() == "wiz":
            player["is_builder"] = True
            print("[DEBUG] wiz è builder")

        if player["password"] != password:
            conn.send("Password errata.\n")
            return None

        conn.send("\nLogin effettuato!\n")

    # =========================
    # REGISTRAZIONE
    # =========================
    elif choice == "2":

        name = await ask(conn, "Nome: ")
        password = await ask(conn, "Password: ")
        race = await ask(conn, "Razza (umano/elfo): ")
        pclass = await ask(conn, "Classe (guerriero/mago): ")

        player = {
            "name": name,
            "password": password,
            "race": race or "umano",
            "class": pclass or "guerriero",
            "level": 1,
            "xp": 0,
            "hp": 100,
            "room": 1001,
            "inventory": [],
            "equipment": {},
            "gold": 0,
            "skills": [] # 🔥 già inizializzato
            
        }

        create_player(player)

        conn.send("\nPersonaggio creato!\n")

    else:
        conn.send("Scelta non valida.\n")
        return None

    # =========================
    # INIT PLAYER (SKILLS SAFE)
    # =========================
    player.setdefault("skills", [])
    player.setdefault("gold", 0)
    unlock_skills(player, conn)
    

    # =========================
    # SPAWN
    # =========================
    spawn_player(player)

    # =========================
    # LOOK
    # =========================
    from commands.look import render_room
    conn.send(render_room(player))

    return player