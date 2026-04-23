from core.lua_engine import run_lua

mob = {"hp": 40}
target = {"name": "player", "hp": 100}

result = run_lua("scripts/boss_test.lua", mob["hp"])

print("RISULTATO:", result)

if not result:
    exit()

# PARSE AZIONE
action, value = result.split(":")
value = int(value)

if action == "ATTACK":
    target["hp"] -= value
    print(f"Attacco normale: {value} danni")

elif action == "FIRE":
    target["hp"] -= value
    print(f"🔥 Fuoco: {value} danni")

print("HP player:", target["hp"])