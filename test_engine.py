from engine.entity import Entity
from engine.event_bus import EventBus
from engine.registry import Registry

from components.stats_component import StatsComponent
from components.combat_component import CombatComponent
from components.inventory_component import InventoryComponent

from systems.stat_system import StatSystem
from systems.combat_system import CombatSystem

# Event bus globale
Registry.event_bus = EventBus()

# Systems
stat_system = StatSystem()
combat_system = CombatSystem(stat_system)


player = Entity(1, "Hero")

player.add_component(
    StatsComponent()
)

player.add_component(
    CombatComponent()
)

player.add_component(
    InventoryComponent()
)


goblin = Entity(2, "Goblin")

goblin.add_component(
    StatsComponent()
)

goblin.add_component(
    CombatComponent()
)


player_stats = player.get_component(
    "StatsComponent"
)

goblin_stats = goblin.get_component(
    "StatsComponent"
)

player_stats.attack_power = 15
goblin_stats.defense = 3
goblin_stats.hp = 40


def on_entity_killed(data):

    print(
        f"{data['target'].name} è morto!"
    )

Registry.event_bus.subscribe(
    "entity_killed",
    on_entity_killed
)


while goblin_stats.hp > 0:

    combat_system.attack(
        player,
        goblin
    )

    print(
        f"HP Goblin: {goblin_stats.hp}"
    )