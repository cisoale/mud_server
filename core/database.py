import sqlite3
import json

conn = sqlite3.connect("mud.db")
cursor = conn.cursor()


def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        name TEXT PRIMARY KEY,
        password TEXT,
        sex TEXT,
        race TEXT,
        class TEXT,
        level INTEGER,
        xp INTEGER,
        xp_to_next INTEGER,
        hp INTEGER,
        max_hp INTEGER,
        inventory TEXT,
        equipment TEXT
    )
    """)
    conn.commit()


def create_player(player):
    cursor.execute("""
    INSERT INTO players (
        name, password, sex, race, class,
        level, xp, xp_to_next,
        hp, max_hp,
        inventory, equipment
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        player["name"],
        player["password"],
        player["sex"],
        player["race"],
        player["class"],
        player.get("level", 1),
        player.get("xp", 0),
        player.get("xp_to_next", 100),
        player.get("hp", 20),
        player.get("max_hp", 20),
        json.dumps(player.get("inventory", [])),
        json.dumps(player.get("equipment", {}))
    ))
    conn.commit()


def get_player(name):
    cursor.execute("SELECT * FROM players WHERE name = ?", (name,))
    row = cursor.fetchone()

    if not row:
        return None

    return {
        "name": row[0],
        "password": row[1],
        "sex": row[2],
        "race": row[3],
        "class": row[4],
        "level": row[5],
        "xp": row[6],
        "xp_to_next": row[7],
        "hp": row[8],
        "max_hp": row[9],
        "inventory": json.loads(row[10]) if row[10] else [],
        "equipment": json.loads(row[11]) if row[11] else {}
    }


def save_player(player):
    cursor.execute("""
    UPDATE players SET
        level = ?,
        xp = ?,
        xp_to_next = ?,
        hp = ?,
        max_hp = ?,
        inventory = ?,
        equipment = ?
    WHERE name = ?
    """, (
        player["level"],
        player["xp"],
        player["xp_to_next"],
        player["hp"],
        player["max_hp"],
        json.dumps(player["inventory"]),
        json.dumps(player["equipment"]),
        player["name"]
    ))
    conn.commit()