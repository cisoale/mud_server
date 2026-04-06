import sqlite3

conn = sqlite3.connect("mud.db")
cursor = conn.cursor()


def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        name TEXT PRIMARY KEY,
        password TEXT,
        sex TEXT,
        race TEXT,
        class TEXT
    )
    """)
    conn.commit()


def create_player(player):
    cursor.execute("""
    INSERT INTO players (name, password, sex, race, class)
    VALUES (?, ?, ?, ?, ?)
    """, (
        player["name"],
        player["password"],
        player["sex"],
        player["race"],
        player["class"]
    ))
    conn.commit()


def get_player(name):
    cursor.execute(
        "SELECT name, password, sex, race, class FROM players WHERE name = ?",
        (name,)
    )

    row = cursor.fetchone()

    if not row:
        return None

    return {
        "name": row[0],
        "password": row[1],
        "sex": row[2],
        "race": row[3],
        "class": row[4]
    }