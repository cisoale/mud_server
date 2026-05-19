class EquipmentSystem:

    # =========================
    # GET COMPONENTS
    # =========================

    def get_equipment(self, entity):

        return entity.get(
            "components",
            {}
        ).get(
            "EquipmentComponent"
        )

    def get_stats(self, entity):

        return entity.get(
            "components",
            {}
        ).get(
            "StatsComponent"
        )

    # =========================
    # RECALCULATE
    # =========================

    def recalculate(self, entity):

        equipment = self.get_equipment(
            entity
        )

        stats = self.get_stats(
            entity
        )

        if not equipment or not stats:
            return

        # reset
        equipment.total_attack = 0
        equipment.total_defense = 0

        equipment.total_strength = 0
        equipment.total_dexterity = 0
        equipment.total_intelligence = 0
        equipment.total_vitality = 0

        # =========================
        # ITEMS
        # =========================

        for item in equipment.slots.values():

            if not item:
                continue

            equipment.total_attack += item.get(
                "attack",
                0
            )

            equipment.total_defense += item.get(
                "defense",
                0
            )

            equipment.total_strength += item.get(
                "strength",
                0
            )

            equipment.total_dexterity += item.get(
                "dexterity",
                0
            )

            equipment.total_intelligence += item.get(
                "intelligence",
                0
            )

            equipment.total_vitality += item.get(
                "vitality",
                0
            )

        # =========================
        # APPLY TO STATS
        # =========================

        stats.bonus_attack = (
            equipment.total_attack
        )

        stats.bonus_defense = (
            equipment.total_defense
        )

        stats.bonus_strength = (
            equipment.total_strength
        )

        # hp bonus vitality
        stats.max_hp = (
            100
            + equipment.total_vitality * 10
        )

        # sync legacy
        entity["max_hp"] = stats.max_hp

    # =========================
    # EQUIP
    # =========================

    def equip(
        self,
        entity,
        slot,
        item
    ):

        equipment = self.get_equipment(
            entity
        )

        if not equipment:
            return False

        equipment.slots[slot] = item

        self.recalculate(entity)

        return True