def get_total_weight(player):
    total = 0

    for item in player.get("inventory", []):
        if isinstance(item, dict):
            total += item.get("weight", 1)

    return total


def can_carry(player, item):
    weight = item.get("weight", 1)
    total = get_total_weight(player)

    return (total + weight) <= player.get("max_weight", 50)


def add_item(player, item):
    if not can_carry(player, item):
        return False

    player.setdefault("inventory", []).append(item)
    return True


def remove_item(player, item_name):
    inv = player.get("inventory", [])

    for item in inv:
        name = item.get("name") if isinstance(item, dict) else str(item)

        if item_name in name:
            inv.remove(item)
            return item

    return None