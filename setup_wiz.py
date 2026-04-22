import sqlite3

conn = sqlite3.connect("data/players.db")
cur = conn.cursor()

cur.execute("UPDATE players SET role='builder' WHERE name='wiz'")

conn.commit()
conn.close()

print("wiz ora è builder")