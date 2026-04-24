def get_total_weight(player):
    total = 0

    for item in player.get("inventory", []):
        if isinstance(item, dict):
            weight = item.get("weight", 1)
            qty = item.get("quantity", 1)
            total += weight * qty

    return total


# =========================
# CARRY CHECK
# =========================
def can_carry(player, item_name, quantity=1, item_data=None):

    if not item_data:
        item_data = {}

    weight = item_data.get("weight", 1)
    total = get_total_weight(player)

    return (total + (weight * quantity)) <= player.get("max_weight", 50)


# =========================
# ADD ITEM (STACK)
# =========================
def add_item(player, item_name, quantity=1):

    inv = player.setdefault("inventory", [])

    # stack
    for item in inv:
        if item["name"] == item_name:
            item["quantity"] += quantity
            return

    inv.append({
        "name": item_name,
        "quantity": quantity
    })


# =========================
# REMOVE ITEM
# =========================
def remove_item(player, item_name, quantity=1):

    inventory = player.get("inventory", [])

    for item in inventory:
        if item["name"] == item_name:

            if item["quantity"] < quantity:
                return False

            item["quantity"] -= quantity

            if item["quantity"] <= 0:
                inventory.remove(item)

            return True

    return False


# =========================
# FIND ITEM
# =========================
def find_item(player, name):

    name = name.lower()

    for item in player.get("inventory", []):

        item_name = item.get("name", "").lower()
        display = item.get("display_name", "").lower()

        if name in item_name or name in display:
            return item

    return None


# =========================
# FORMAT INVENTORY
# =========================
def format_inventory(player):

    inv = player.get("inventory", [])

    if not inv:
        return "Inventario vuoto.\n"

    lines = ["--- Inventario ---"]

    for item in inv:
        name = item.get("display_name", item.get("name"))
        qty = item.get("quantity", 1)

        lines.append(f"{name} x{qty}")

    return "\n".join(lines) + "\n"