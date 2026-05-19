from engine.component import Component


class CombatComponent(Component):

    def __init__(self):

        # combat state
        self.in_combat = False

        # targets
        self.target_id = None

        # timers
        self.last_attack_time = 0

        self.attack_cooldown = 2.0

        # combat flags
        self.stunned = False
        self.silenced = False
        self.rooted = False

        # threat
        self.threat_table = {}

        # combo system
        self.combo_points = 0

        # cast
        self.casting = False
        self.cast_end_time = 0

        # combat stats
        self.attack_speed = 1.0
        self.crit_bonus = 0

        # runtime
        self.last_attacker_id = None