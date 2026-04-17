def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        name TEXT PRIMARY KEY,
        password TEXT,
        race TEXT,
        classe TEXT,
        level INTEGER,
        xp INTEGER,
        hp INTEGER,
        max_hp INTEGER,
        room INTEGER,
        inventory TEXT,
        equipment TEXT,
        builder INTEGER
    )
    """)

    conn.commit()
    conn.close()