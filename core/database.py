import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "../players.db")


# =========================
# INIT DB
# =========================
def init_db():
    """
    Inizializza il database e garantisce tutte le colonne necessarie
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # =========================
    # CREAZIONE BASE
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        name TEXT PRIMARY KEY,
        password TEXT,
        race TEXT,
        class TEXT,
        level INTEGER,
        xp INTEGER,
        hp INTEGER,
        room INTEGER,
        inventory TEXT,
        equipment TEXT,
        gold INTEGER DEFAULT 0
    )
    """)

    # =========================
    # MIGRAZIONE (se gold manca)
    # =========================
    cursor.execute("PRAGMA table_info(players)")
    columns = [col[1] for col in cursor.fetchall()]

    if "gold" not in columns:
        print("[DB] Aggiunta colonna GOLD")
        cursor.execute("ALTER TABLE players ADD COLUMN gold INTEGER DEFAULT 0")

    conn.commit()
    conn.close()


# =========================
# GET PLAYER
# =========================
def get_player(name):
    """
    Recupera player dal database
    """

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players WHERE name = ?", (name,))
    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    try:
        player = {
            "name": row["name"],
            "password": row["password"],
            "race": row["race"],
            "class": row["class"],
            "level": row["level"],
            "xp": row["xp"],
            "hp": row["hp"],
            "room": row["room"],

            "inventory": json.loads(row["inventory"] or "[]"),
            "equipment": json.loads(row["equipment"] or "{}"),

            "gold": row["gold"] if "gold" in row.keys() else 0,

            "builder": 0
        }

        print(f"[LOAD] {player['name']} GOLD={player['gold']}")

        return player

    except Exception as e:
        print(f"[DB LOAD ERROR] {name}: {e}")
        return None


# =========================
# CREATE PLAYER
# =========================
def create_player(player):
    """
    Crea un nuovo player nel database
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    room = player.get("room", 1001)

    if hasattr(room, "vnum"):
        room = room.vnum

    try:
        cursor.execute("""
        INSERT INTO players (
            name, password, race, class,
            level, xp, hp, room,
            inventory, equipment, gold
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            player["name"],
            player["password"],
            player.get("race", "umano"),
            player.get("class", "guerriero"),
            player.get("level", 1),
            player.get("xp", 0),
            player.get("hp", 100),
            room,
            json.dumps(player.get("inventory", [])),
            json.dumps(player.get("equipment", {})),
            player.get("gold", 0)
        ))

        conn.commit()
        print(f"[DB] Creato player: {player['name']}")

    except Exception as e:
        print(f"[DB CREATE ERROR] {player.get('name')}: {e}")

    finally:
        conn.close()


# =========================
# SAVE PLAYER
# =========================
def save_player_to_db(player):
    """
    Salva player nel database
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    room = player.get("room", 1001)

    if hasattr(room, "vnum"):
        room = room.vnum

    try:
        cursor.execute("""
        UPDATE players SET
            level = ?,
            xp = ?,
            hp = ?,
            room = ?,
            inventory = ?,
            equipment = ?,
            gold = ?
        WHERE name = ?
        """, (
            player.get("level", 1),
            player.get("xp", 0),
            player.get("hp", 100),
            room,
            json.dumps(player.get("inventory", [])),
            json.dumps(player.get("equipment", {})),
            player.get("gold", 0),
            player.get("name")
        ))

        conn.commit()

        print(
            f"[DB SAVE] {player.get('name')} | "
            f"GOLD={player.get('gold', 0)} | XP={player.get('xp', 0)}"
        )

    except Exception as e:
        print(f"[DB SAVE ERROR] {player.get('name')}: {e}")

    finally:
        conn.close()