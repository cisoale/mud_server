def create_mob(name, description, hp, inventory=None):
    return {
        "name": name,
        "description": description,
        "hp": hp,
        "max_hp": hp,
        "inventory": inventory or []
    }