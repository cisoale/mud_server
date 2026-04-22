import time
from core.database import save_player_to_db

SAVE_COOLDOWN = 5


def save_player(player):
    save_player_to_db(player)
    print(f"[SAVE] {player['name']}")


def auto_save(player):

    now = time.time()

    if not player.get("last_save"):
        player["last_save"] = 0

    if now - player["last_save"] >= SAVE_COOLDOWN:
        save_player(player)
        player["last_save"] = now