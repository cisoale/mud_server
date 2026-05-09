from engine.component import Component

class CombatComponent(Component):
    def __init__(self,
                 max_hp=100,
                 attack=10,
                 defense=5):

        self.max_hp = max_hp
        self.hp = max_hp

        self.attack = attack
        self.defense = defense

        self.dead = False