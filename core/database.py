import sqlite3

conn = sqlite3.connect("mud.db")

def create_player(name, password, sex, race, cls):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO players (name, password, sex, race, class)
        VALUES (?, ?, ?, ?, ?)
    """, (name, password, sex, race, cls))

    conn.commit()
    return load_player(name)