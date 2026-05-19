import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(
    PROJECT_DIR,
    "data"
)

ROOMS_DIR = os.path.join(
    DATA_DIR,
    "rooms"
)

MOBS_DIR = os.path.join(
    DATA_DIR,
    "mobs"
)

ITEMS_DIR = os.path.join(
    DATA_DIR,
    "items"
)

print("PROJECT_DIR =", PROJECT_DIR)
print("DATA_DIR =", DATA_DIR)
print("ROOMS_DIR =", ROOMS_DIR)
print("MOBS_DIR =", MOBS_DIR)
print("ITEMS_DIR =", ITEMS_DIR)