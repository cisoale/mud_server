from engine.component import Component


class EquipmentComponent(Component):

    def __init__(self):

        self.slots = {

            "head": None,
            "chest": None,
            "legs": None,
            "feet": None,

            "main_hand": None,
            "off_hand": None,

            "ring_1": None,
            "ring_2": None,

            "amulet": None
        }