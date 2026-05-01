import sqlite3

conn = sqlite3.connect("players.db")
cursor = conn.cursor()

cursor.execute("UPDATE players SET builder = 1 WHERE name = ?", ("wiz",))

conn.commit()
conn.close()

print("wiz è ora builder!")