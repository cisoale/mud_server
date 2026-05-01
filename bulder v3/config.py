import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 👉 METTI IL PATH REALE DEL TUO MUD
MUD_ROOT = r"C:\Users\Ale\Desktop\Realm of Lord\mud_server"

DATA_DIR = os.path.join(MUD_ROOT, "data")

MOBS_DIR = os.path.join(DATA_DIR, "mobs")
ITEMS_DIR = os.path.join(DATA_DIR, "items")
ROOMS_DIR = os.path.join(DATA_DIR, "rooms")