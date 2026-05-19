class StatSystem:

    # =========================
    # GET STATS COMPONENT
    # =========================

    def get_stats(self, entity):

        if not entity:
            return None

        components = entity.get(
            "components",
            {}
        )

        return components.get(
            "StatsComponent"
        )

    # =========================
    # HP
    # =========================

    def get_hp(self, entity):

        stats = self.get_stats(entity)

        # ECS
        if stats:
            return stats.hp

        # LEGACY
        if "current_hp" in entity:
            return entity["current_hp"]

        return entity.get("hp", 1)

    # =========================
    # MAX HP
    # =========================

    def get_max_hp(self, entity):

        stats = self.get_stats(entity)

        if stats:
            return stats.max_hp

        return entity.get(
            "max_hp",
            entity.get("hp", 1)
        )

    # =========================
    # ATTACK
    # =========================

    def get_attack(self, entity):

        stats = self.get_stats(entity)

        if stats:

            return (
                stats.attack_power
                + stats.bonus_attack
                + stats.strength
            )

        return entity.get(
            "damage",
            1
        )

    # =========================
    # DEFENSE
    # =========================

    def get_defense(self, entity):

        stats = self.get_stats(entity)

        if stats:

            return (
                stats.defense
                + stats.bonus_defense
            )

        return entity.get(
            "defense",
            0
        )

    # =========================
    # DAMAGE
    # =========================

    def damage(
        self,
        entity,
        amount
    ):

        stats = self.get_stats(entity)

        # =========================
        # ECS
        # =========================

        if stats:

            stats.hp -= amount

            entity["hp"] = stats.hp
            entity["current_hp"] = stats.hp

            return

        # =========================
        # LEGACY current_hp
        # =========================

        if "current_hp" in entity:

            entity["current_hp"] -= amount
            entity["hp"] = entity["current_hp"]

            return

        # =========================
        # LEGACY hp only
        # =========================

        if "hp" in entity:

            entity["hp"] -= amount

    # =========================
    # HEAL
    # =========================

    def heal(
        self,
        entity,
        amount
    ):

        stats = self.get_stats(entity)

        # ECS
        if stats:

            stats.hp += amount

            if stats.hp > stats.max_hp:
                stats.hp = stats.max_hp

            entity["hp"] = stats.hp
            entity["current_hp"] = stats.hp

            return

        # LEGACY
        if "current_hp" in entity:

            entity["current_hp"] += amount

            max_hp = entity.get(
                "max_hp",
                100
            )

            if entity["current_hp"] > max_hp:
                entity["current_hp"] = max_hp

            entity["hp"] = entity["current_hp"]

            return

        if "hp" in entity:

            entity["hp"] += amount