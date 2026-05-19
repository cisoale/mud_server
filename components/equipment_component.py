from engine.component import Component


class EquipmentComponent(Component):

    def __init__(self):

        # equipment slots
        self.slots = {

            "weapon": None,
            "head": None,
            "chest": None,
            "legs": None,
            "feet": None,
            "hands": None,

            "ring1": None,
            "ring2": None,

            "neck": None,
            "cloak": None

        }

        # cached bonuses
        self.total_attack = 0
        self.total_defense = 0

        self.total_strength = 0
        self.total_dexterity = 0
        self.total_intelligence = 0
        self.total_vitality = 0

        # resistances
        self.fire_resistance = 0
        self.ice_resistance = 0
        self.poison_resistance = 0