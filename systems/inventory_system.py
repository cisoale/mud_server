class InventorySystem:

    def add_item(self, entity, item):

        inventory = entity.get_component(
            "InventoryComponent"
        )

        if not inventory:
            return False

        if len(inventory.items) >= inventory.max_slots:
            return False

        inventory.items.append(item)

        inventory.current_weight += item.weight

        return True