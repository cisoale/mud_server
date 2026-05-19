class CombatSystem:

    def __init__(self, stat_system):

        self.stat_system = stat_system

    def attack(
        self,
        attacker,
        target
    ):

        atk_stats = self.stat_system.get_final_stats(
            attacker
        )

        tgt_stats = self.stat_system.get_final_stats(
            target
        )

        damage = max(
            1,
            atk_stats["attack"]
            - tgt_stats["defense"]
        )

        target_stats = target.get_component(
            "StatsComponent"
        )

        target_stats.hp -= damage