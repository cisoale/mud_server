local input = io.read("*all")
local hp = tonumber(input) or 100

math.randomseed(os.time())

-- FASE 2
if hp < 50 then
    print("FIRE:30")
    return
end

-- FASE 1
local roll = math.random()

if roll < 0.5 then
    print("ATTACK:10")
else
    print("FIRE:20")
end