import json
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "database.db")


def get_connection():
    return sqlite3.connect(DB_PATH)

# =========================
# INIT DB
# =========================
def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        name TEXT PRIMARY KEY,
        password TEXT,
        room INTEGER,
        hp INTEGER,
        max_hp INTEGER,
        xp INTEGER,
        level INTEGER,
        inventory TEXT,
        equipment TEXT,
        builder INTEGER
    )
    """)

    conn.commit()
    conn.close()


# =========================
# CREATE PLAYER
# =========================
def create_player(name, password, race, classe):

    import sqlite3

    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO players (
            name, password, race, classe,
            level, xp, hp, room, inventory, equipment
        )
        VALUES (?, ?, ?, ?, 1, 0, 100, 1001, '[]', '{}')
    """, (name, password, race, classe))

    conn.commit()
    conn.close()

# =========================
# GET PLAYER
# =========================
def get_player(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players WHERE name = ?", (name,))
    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return {
        "name": row[0],
        "password": row[1],
        "room": row[2],
        "hp": row[3],
        "max_hp": row[4],
        "xp": row[5],
        "level": row[6],
        "inventory": json.loads(row[7]),
        "equipment": json.loads(row[8]),
        "builder": bool(row[9])
    }


# =========================
# SAVE PLAYER
# =========================
def save_player(player):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE players SET
        room = ?,
        hp = ?,
        max_hp = ?,
        xp = ?,
        level = ?,
        inventory = ?,
        equipment = ?
    WHERE name = ?
    """, (
        player["room"],
        player["hp"],
        player["max_hp"],
        player["xp"],
        player["level"],
        json.dumps(player["inventory"]),
        json.dumps(player["equipment"]),
        player["name"]
    ))

    conn.commit()
    conn.close()

def make_builder(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE players SET builder = 1 WHERE name = ?",
        (name,)
    )

    conn.commit()
    conn.close()