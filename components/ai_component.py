from engine.component import Component


class AIComponent(Component):

    def __init__(
        self,
        brain_type="passive",
        aggro_range=3,
        leash_range=10
    ):

        # brain
        self.brain_type = brain_type

        # state
        self.state = "idle"

        # combat
        self.target = None
        self.last_attacker = None

        # aggro
        self.threat_table = {}

        # movement
        self.home_room = None
        self.spawn_room = None

        # patrol
        self.patrol_points = []
        self.current_patrol_index = 0

        # range
        self.aggro_range = aggro_range
        self.leash_range = leash_range

        # behavior
        self.can_flee = False
        self.can_patrol = False
        self.can_call_help = False

        # social
        self.faction = None

        # memory
        self.memory = {}

        # timing
        self.last_think = 0
        self.think_interval = 2