def create_mob(name, description, hp, inventory=None, xp=20):
    return {
        "name": name,
        "description": description,
        "hp": hp,
        "max_hp": hp,
        "inventory": inventory or [],
        "xp": xp
    }