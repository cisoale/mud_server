import time

from systems.stat_system import StatSystem


stat_system = StatSystem()


class EffectsSystem:

    # =========================
    # COMPONENT
    # =========================

    def get_effects(self, entity):

        return entity.get(
            "components",
            {}
        ).get(
            "EffectsComponent"
        )

    # =========================
    # ADD EFFECT
    # =========================

    def add_effect(
        self,
        entity,
        effect_type,
        duration,
        power=1
    ):

        effects = self.get_effects(entity)

        if not effects:
            return

        # immunity
        if effect_type in effects.immunities:
            return

        effect = {

            "type": effect_type,

            "power": power,

            "start": time.time(),

            "duration": duration
        }

        effects.effects.append(effect)

        print(
            f"[EFFECT] "
            f"{entity['name']} "
            f"+ {effect_type}"
        )

    # =========================
    # PROCESS
    # =========================

    def process(self, entity):

        effects = self.get_effects(entity)

        if not effects:
            return

        now = time.time()

        remaining = []

        for effect in effects.effects:

            elapsed = (
                now - effect["start"]
            )

            if elapsed >= effect["duration"]:

                print(
                    f"[EFFECT END] "
                    f"{entity['name']} "
                    f"- {effect['type']}"
                )

                continue

            # =====================
            # POISON
            # =====================

            if effect["type"] == "poison":

                stat_system.damage(
                    entity,
                    effect["power"]
                )

            # =====================
            # REGEN
            # =====================

            elif effect["type"] == "regen":

                stat_system.heal(
                    entity,
                    effect["power"]
                )

            remaining.append(effect)

        effects.effects = remaining