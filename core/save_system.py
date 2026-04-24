import time
from core.database import save_player_to_db

SAVE_COOLDOWN = 5


def save_player(player):
    """
    Salva player in modo sicuro
    """

    if not player:
        print("[SAVE ERROR] player nullo")
        return

    try:
        save_player_to_db(player)

        print(
            f"[SAVE] {player.get('name')} | "
            f"GOLD={player.get('gold', 0)} | "
            f"XP={player.get('xp', 0)}"
        )

    except Exception as e:
        print(f"[SAVE ERROR] {player.get('name')}: {e}")


def auto_save(player):
    """
    Salvataggio automatico con cooldown
    """

    if not player:
        return

    now = time.time()

    if not player.get("last_save"):
        player["last_save"] = 0

    if now - player["last_save"] >= SAVE_COOLDOWN:
        save_player(player)
        player["last_save"] = now