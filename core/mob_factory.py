import copy
import uuid

from components.stats_component import StatsComponent
from components.ai_component import AIComponent
from components.position_component import PositionComponent
from components.inventory_component import InventoryComponent
from components.equipment_component import EquipmentComponent
from components.effects_component import EffectsComponent
from components.combat_component import CombatComponent

def create_mob(template):

    mob = copy.deepcopy(template)

    # =========================
    # RUNTIME DATA
    # =========================

    mob["entity_id"] = str(uuid.uuid4())

    mob["current_hp"] = mob.get("hp", 10)

    mob["alive"] = True

    mob["effects"] = []

    mob["inventory"] = mob.get(
        "inventory",
        []
    )

    # =========================
    # ECS COMPONENTS
    # =========================

    mob["components"] = {
        "EquipmentComponent": EquipmentComponent(),
        "CombatComponent": CombatComponent(),
    }
    
    # stats
    stats = StatsComponent()

    stats.max_hp = mob.get("hp", 10)
    stats.hp = mob.get("hp", 10)

    stats.attack_power = mob.get(
        "damage",
        1
    )

    stats.defense = mob.get(
        "defense",
        0
    )

    mob["components"][
        "StatsComponent"
    ] = stats

    # AI
    ai = AIComponent()

    if mob.get("aggressive"):
        ai.brain_type = "aggressive"

    mob["components"][
        "AIComponent"
    ] = ai

    # position
    position = PositionComponent()

    mob["components"][
        "PositionComponent"
    ] = position

    # inventory
    inventory = InventoryComponent()

    inventory.items = list(
        mob.get("inventory", [])
    )

    inventory.gold = mob.get(
        "gold",
        0
    )

    mob["components"][
        "InventoryComponent"
    ] = inventory
 # DEBUG
    print(
        f"[ECS] Mob creato: "
        f"{mob['name']} -> "
        f"{list(mob['components'].keys())}"
    )
    return mob