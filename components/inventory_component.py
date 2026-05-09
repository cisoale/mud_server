from engine.component import Component


class InventoryComponent(Component):

    def __init__(
        self,
        max_slots=20,
        max_weight=100
    ):

        # items
        self.items = []

        # limits
        self.max_slots = max_slots
        self.max_weight = max_weight

        # weight
        self.current_weight = 0

        # currency
        self.gold = 0

        # flags
        self.locked = False
        self.shared = False

        # ownership
        self.owner_id = None