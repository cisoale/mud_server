import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "../players.db")


# =========================
# INIT DB
# =========================
def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

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
        equipment TEXT
    )
    """)

    conn.commit()
    conn.close()


# =========================
# GET PLAYER
# =========================
def get_player(name):
    import sqlite3

    conn = sqlite3.connect("players.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM players WHERE name = ?", (name,))
    row = cur.fetchone()

    conn.close()

    if not row:
        return None

    player = dict(row)

    # 🔥 FIX SICURO
    player["builder"] = player.get("builder", 0)

    
    return {
        "name": row[0],
        "password": row[1],
        "race": row[2],
        "class": row[3],
        "level": row[4],
        "xp": row[5],
        "hp": row[6],
        "room": row[7],  # ✔ SEMPRE INT
        "inventory": json.loads(row[8] or "[]"),
        "equipment": json.loads(row[9] or "{}"),
        "builder": 0
    }


# =========================
# CREATE PLAYER
# =========================
def create_player(player):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    room = player.get("room", 1001)

    # sicurezza
    if hasattr(room, "vnum"):
        room = room.vnum

    cursor.execute("""
    INSERT INTO players (
        name, password, race, class, level, xp, hp, room, inventory, equipment
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        json.dumps(player.get("equipment", {}))
    ))

    conn.commit()
    conn.close()


# =========================
# SAVE PLAYER
# =========================
def save_player_to_db(player):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    room = player.get("room", 1001)

    # 🔥 FIX CRITICO
    if hasattr(room, "vnum"):
        room = room.vnum

    cursor.execute("""
    UPDATE players SET
        level = ?,
        xp = ?,
        hp = ?,
        room = ?,
        inventory = ?,
        equipment = ?
    WHERE name = ?
    """, (
        player.get("level", 1),
        player.get("xp", 0),
        player.get("hp", 100),
        room,
        json.dumps(player.get("inventory", [])),
        json.dumps(player.get("equipment", {})),
        player.get("name")
    ))

    conn.commit()
    conn.close()