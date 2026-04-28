from core.world import get_room
import random


def execute(player, conn, args):

    if not args:
        conn.send("Parlare con chi?\n")
        return

    room = get_room(player["room"])
    if not room:
        conn.send("Errore stanza.\n")
        return

    target_name = args[0].lower()
    choice = args[1] if len(args) > 1 else None

    for mob in room.mobs:

        if not mob.get("npc"):
            continue

        if mob["name"].lower() != target_name:
            continue

        quests = mob.get("quests", [])
        player_quest = player.get("quest")

        # =========================
        # SCELTA QUEST
        # =========================
        if quests and not player_quest:

            # se NON ha scelto ancora
            if not choice:
                conn.send(f"{mob['name']} dice:\n")

                for i, q in enumerate(quests, start=1):
                    conn.send(f"{i}) {q['label']}\n")

                conn.send("Scegli con: talk locandiere <numero>\n")
                return

            # scelta fatta
            try:
                index = int(choice) - 1
                selected = quests[index]
            except:
                conn.send("Scelta non valida.\n")
                return

            player["quest"] = {
                "id": selected["id"],
                "target": selected["target"],
                "required": selected["required"],
                "progress": 0,
                "completed": False,
                "reward_gold": selected["reward_gold"],
                "reward_xp": selected["reward_xp"]
            }

            conn.send(
                f"{mob['name']} dice: \"Uccidi {selected['required']} {selected['target']} per me.\"\n"
            )
            return

        # =========================
        # QUEST COMPLETATA
        # =========================
        if player_quest and player_quest.get("completed"):

            conn.send(f"{mob['name']} dice: \"Ottimo lavoro!\"\n")

            conn.send(
                f"[REWARD] +{player_quest['reward_gold']} gold, +{player_quest['reward_xp']} xp\n"
            )

            player["gold"] += player_quest["reward_gold"]
            player["xp"] += player_quest["reward_xp"]

            player["quest"] = None
            return

        # =========================
        # QUEST IN CORSO
        # =========================
        if player_quest:
            conn.send(
                f"{mob['name']} dice: \"Hai ucciso {player_quest['progress']}/{player_quest['required']} {player_quest['target']}.\"\n"
            )
            return

        # fallback
        dialogues = mob.get("dialogues", [])
        if dialogues:
            conn.send(f"{mob['name']} dice: \"{random.choice(dialogues)}\"\n")
        else:
            conn.send(f"{mob['name']} non ha nulla da dire.\n")

        return

    conn.send("Non trovi nessuno con cui parlare.\n")