def execute(player, conn, args):

    clean = []
    removed = 0

    for item in player.get("inventory", []):
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            clean.append(item)
        else:
            removed += 1

    player["inventory"] = clean

    conn.send(f"Pulizia completata. Rimossi {removed} oggetti corrotti.\n")