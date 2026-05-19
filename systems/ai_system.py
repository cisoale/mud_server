class AISystem:

    def update(self, entity):

        ai = entity.get_component("AIComponent")

        if not ai:
            return

        if ai.state == "idle":
            self.handle_idle(entity, ai)

        elif ai.state == "combat":
            self.handle_combat(entity, ai)

        elif ai.state == "patrol":
            self.handle_patrol(entity, ai)