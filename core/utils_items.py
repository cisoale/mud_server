RARITY_COLOR = {
    "common": "",
    "rare": "[RARE] ",
    "epic": "[EPIC] ",
    "legendary": "[LEGENDARY] "
}


def format_item(item):
    prefix = RARITY_COLOR.get(item.get("rarity", "common"), "")
    return prefix + item["name"]