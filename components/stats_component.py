from engine.component import Component


class StatsComponent(Component):

    def __init__(self):

        # PRIMARY
        self.strength = 10
        self.dexterity = 10
        self.intelligence = 10
        self.vitality = 10

        # HP / MANA
        self.max_hp = 100
        self.hp = 100

        self.max_mana = 50
        self.mana = 50

        self.max_stamina = 100
        self.stamina = 100

        # COMBAT
        self.attack_power = 10
        self.defense = 5

        self.magic_power = 0
        self.magic_defense = 0

        self.crit_chance = 5
        self.crit_damage = 150

        # SPEED
        self.attack_speed = 1.0
        self.move_speed = 1.0

        # REGEN
        self.hp_regen = 1
        self.mana_regen = 1
        self.stamina_regen = 1

        # RESISTANCES
        self.fire_resistance = 0
        self.ice_resistance = 0
        self.poison_resistance = 0

        # BONUS
        self.bonus_strength = 0
        self.bonus_attack = 0
        self.bonus_defense = 0

        # FLAGS
        self.dead = False
        self.invulnerable = False