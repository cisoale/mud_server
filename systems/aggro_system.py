import time

from components.threat_component import ThreatComponent


# =========================
# ADD AGGRO
# =========================

def add_aggro(mob, target, amount):

    if not mob or not target:
        return

    components = mob.get("components", {})

    threat = components.get(
        "ThreatComponent"
    )

    if not threat:
        return

    target_id = id(target)

    threat.add_threat(
        target_id,
        amount
    )

    threat.current_target = target

    threat.in_combat = True

    threat.last_attacked = time.time()


# =========================
# GET TARGET
# =========================

def get_target(mob):

    if not mob:
        return None

    components = mob.get("components", {})

    threat = components.get(
        "ThreatComponent"
    )

    if not threat:
        return None

    return threat.current_target


# =========================
# RESET AGGRO
# =========================

def reset_aggro(mob):

    if not mob:
        return

    components = mob.get("components", {})

    threat = components.get(
        "ThreatComponent"
    )

    if not threat:
        return

    threat.clear()