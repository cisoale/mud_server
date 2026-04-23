import os
from core.lua_engine import run_lua


# =========================
# PARSE LUA RESULT
# =========================
def parse_lua_result(result):

    if not result or ":" not in result:
        return None, None

    try:
        action, value = result.strip().split(":")
        return action.upper(), int(value)
    except Exception:
        print(f"[LUA PARSE ERROR] {result}")
        return None, None


# =========================
# APPLY ACTION
# =========================
def apply_boss_action(mob, target, action, value):

    name = mob.get("name", "Mob")

    if action == "ATTACK":
        target["current_hp"] -= value
        return f"{name} attacca per {value} danni!"

    elif action == "FIRE":
        target["current_hp"] -= value
        return f"{name} lancia una fiammata! ({value} danni)"

    elif action == "HEAL":
        mob["current_hp"] += value
        return f"{name} si cura di {value} HP!"

    return None


# =========================
# MAIN BOSS ACTION
# =========================
def boss_action(mob, target):

    # solo boss
    if mob.get("type") != "boss":
        return None

    script_path = mob.get("script")

    if not script_path:
        return None

    if not os.path.exists(script_path):
        print(f"[LUA ERROR] Script non trovato: {script_path}")
        return None

    # 🔥 usa current_hp (IMPORTANTISSIMO)
    result = run_lua(script_path, mob.get("current_hp", 100))

    if not result:
        return None

    action, value = parse_lua_result(result)

    if not action:
        return None

    # 🔥 QUI ORA FUNZIONA
    return apply_boss_action(mob, target, action, value)