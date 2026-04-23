SET_BONUS = {
    "drago": {
        2: {"str": 2},
        3: {"str": 5, "regen_hp": 2},
        4: {"str": 10, "regen_hp": 5}
    }
}
def get_set_bonus(player):

    equipped = player.get("equipment", {})
    sets = {}

    # conta pezzi
    for item in equipped.values():

        set_name = item.get("set")

        if not set_name:
            continue

        sets[set_name] = sets.get(set_name, 0) + 1

    bonus_totale = {}

    for set_name, count in sets.items():

        bonus_data = SET_BONUS.get(set_name, {})

        for pieces, bonus in bonus_data.items():

            if count >= pieces:

                for stat, value in bonus.items():
                    bonus_totale[stat] = bonus_totale.get(stat, 0) + value

    return bonus_totale