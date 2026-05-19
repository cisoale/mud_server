from components.stats_component import StatsComponent
from components.ai_component import AIComponent
from components.position_component import PositionComponent
from components.inventory_component import InventoryComponent
from components.equipment_component import EquipmentComponent
from components.effects_component import EffectsComponent
from components.combat_component import CombatComponent

# =====================================
# INJECT ECS COMPONENTS
# =====================================

def inject_player_components(player):

    # evita doppio inject
    if "components" in player:
        return player

    # =========================
    # ECS COMPONENTS
    # =========================

    stats = StatsComponent()

    # sync legacy -> ECS
    stats.hp = player.get(
        "hp",
        100
    )

    stats.max_hp = player.get(
        "max_hp",
        stats.hp
    )

    stats.attack_power = player.get(
        "damage",
        5
    )

    stats.defense = player.get(
        "defense",
        0
    )

    # =========================
    # ECS
    # =========================

    player["components"] = {
        
        "CombatComponent": CombatComponent(),
        
        "EffectsComponent": EffectsComponent(),
        
        "StatsComponent": stats,

        "AIComponent": AIComponent(
            brain_type="player"
        ),

        "PositionComponent": PositionComponent(),

        "InventoryComponent": InventoryComponent(),

        "EquipmentComponent": EquipmentComponent()
    }

    # sync current hp
    player["current_hp"] = stats.hp

    print(
        f"[ECS PLAYER] "
        f"{player['name']} -> "
        f"{list(player['components'].keys())}"
    )

    return player