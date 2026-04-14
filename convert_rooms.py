import json
import os

os.makedirs("data/rooms", exist_ok=True)

with open("data/rooms.json") as f:
    rooms = json.load(f)

for r in rooms:
    vnum = r["vnum"]
    with open(f"data/rooms/{vnum}.json", "w") as f:
        json.dump(r, f, indent=4)

print("Conversione completata")