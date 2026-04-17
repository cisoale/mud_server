import json
from core.database import save_player

def auto_save(player):
    try:
        save_player(player)
    except Exception as e:
        print(f"[SAVE ERROR] {e}")