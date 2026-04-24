math.randomseed(os.time())

local drops = {}

if math.random() < 0.5 then
    table.insert(drops, "potion:1")
end

if math.random() < 0.2 then
    table.insert(drops, "gold_ring:1")
end

print(table.concat(drops, ","))