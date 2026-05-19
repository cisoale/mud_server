from engine.component import Component


class PositionComponent(Component):

    def __init__(self):

        # room
        self.room_id = None
        self.last_room_id = None

        # coordinates
        self.x = 0
        self.y = 0
        self.z = 0

        # movement
        self.moving = False
        self.facing = "north"

        # terrain
        self.terrain = None
        self.region = None

        # tracking
        self.last_positions = []

        # zones
        self.safe_zone = False
        self.pvp_zone = False