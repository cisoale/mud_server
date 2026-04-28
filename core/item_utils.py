def normalize_item(item):
    """Converte item sporchi (stringhe o dict incompleti)"""
    if isinstance(item, str):
        return {
            "name": item.replace(" ", "_"),
            "display_name": item.title(),
            "quantity": 1,
            "stackable": True
        }

    if isinstance(item, dict):
        if "name" not in item:
            return None

        item.setdefault("display_name", item["name"].replace("_", " ").title())
        item.setdefault("quantity", 1)
        item.setdefault("stackable", False)

        return item

    return None


def add_item(container, new_item):
    """Aggiunge item con stack automatico"""

    item = normalize_item(new_item)
    if not item:
        return False

    name = item["name"]
    qty = item.get("quantity", 1)
    stackable = item.get("stackable", False)

    # STACK
    if stackable:
        for existing in container:
            if (
                isinstance(existing, dict)
                and existing.get("name") == name
                and existing.get("stackable", False)
            ):
                existing["quantity"] += qty
                return True

    # NO STACK
    container.append(item.copy())
    return True