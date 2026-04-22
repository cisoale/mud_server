import copy

def create_mob(template):

    mob = copy.deepcopy(template)

    mob["current_hp"] = mob.get("hp", 10)
    mob["alive"] = True
    mob["effects"] = []
    mob["inventory"] = mob.get("inventory", [])

    return mob