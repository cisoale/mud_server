from engine.component import Component


class EffectsComponent(Component):

    def __init__(self):

        # active effects
        self.effects = []

        # immunities
        self.immunities = set()

        # resistances
        self.resistances = {

            "poison": 0,
            "fire": 0,
            "ice": 0,
            "bleed": 0,
            "curse": 0

        }