def execute(player, conn, args):

    if not args:
        conn.send("Cosa vuoi bere?\n")
        return

    name = " ".join(args).lower()

    for item in player["inventory"]:

        if item["name"].lower() == name:

            if item.get("type") != "consumable":
                conn.send("Non è consumabile.\n")
                return

            effects = item.get("effects", {})

            if "hp" in effects:
                player["hp"] += effects["hp"]
                conn.send(f"Recuperi {effects['hp']} HP.\n")

            if "mana" in effects:
                player["mana"] += effects["mana"]

            item["quantity"] -= 1

            if item["quantity"] <= 0:
                player["inventory"].remove(item)

            return

    conn.send("Non lo hai.\n")