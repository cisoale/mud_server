def get_item_effects(player):

    effects = {}

    for item in player.get("equipment", {}).values():

        for k, v in item.get("effects", {}).items():
            effects[k] = effects.get(k, 0) + v

    return effects