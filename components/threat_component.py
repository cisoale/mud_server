from engine.component import Component


class ThreatComponent(Component):

    def __init__(self):

        # =========================
        # THREAT TABLE
        # player_id -> threat value
        # =========================

        self.threat_table = {}

        # =========================
        # TARGET ATTUALE
        # =========================

        self.current_target = None

        # =========================
        # ROOM ORIGINALE
        # =========================

        self.home_room = None

        # =========================
        # STATO COMBAT
        # =========================

        self.in_combat = False

        # =========================
        # TIMER RESET
        # =========================

        self.last_attacked = 0

    # =========================
    # ADD THREAT
    # =========================

    def add_threat(self, target_id, amount):

        if target_id not in self.threat_table:
            self.threat_table[target_id] = 0

        self.threat_table[target_id] += amount

    # =========================
    # REMOVE TARGET
    # =========================

    def remove_target(self, target_id):

        if target_id in self.threat_table:
            del self.threat_table[target_id]

    # =========================
    # CLEAR
    # =========================

    def clear(self):

        self.threat_table = {}
        self.current_target = None
        self.in_combat = False

    # =========================
    # GET TOP TARGET
    # =========================

    def get_top_target(self):

        if not self.threat_table:
            return None

        return max(
            self.threat_table,
            key=self.threat_table.get
        )