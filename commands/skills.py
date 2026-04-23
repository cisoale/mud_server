def execute(player, conn, args):

    skills = player.get("skills", [])

    if not skills:
        conn.send("Non hai abilità.\n")
        return

    conn.send("\n--- ABILITÀ ---\n")

    for s in skills:
        conn.send(f"- {s['name']}\n")