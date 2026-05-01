function safeJSON(str) {
    try { return JSON.parse(str); }
    catch { return {}; }
}

async function loadMobs() {
    const data = await API.get("/mobs");
    state.mobs = data.mobs || [];
    renderMobs();
}

function renderMobs() {
    mobList.innerHTML = "";

    state.mobs.forEach(m => {
        let d = document.createElement("div");
        d.className = "item";
        d.innerText = m.name;

        d.onclick = () => {
            state.current.mob = m;

            mob_name.value = m.name || "";
            mob_level.value = m.level || 1;
            mob_hp.value = m.hp || 10;
            mob_damage.value = m.damage || 1;
            mob_defense.value = m.defense || 0;

            mob_xp.value = m.xp || 10;

            mob_gold_min.value = m.gold_min || 0;
            mob_gold_max.value = m.gold_max || 0;

            mob_loot.value = JSON.stringify(m.loot || [], null, 2);
            mob_ai.value = JSON.stringify(m.ai || {}, null, 2);
            mob_flags.value = JSON.stringify(m.flags || [], null, 2);
            mob_spawn.value = JSON.stringify(m.spawn || {}, null, 2);
        };

        mobList.appendChild(d);
    });
}

function newMob() {
    state.current.mob = null;
    document.querySelectorAll(".editor input, .editor textarea").forEach(e => e.value = "");
}

async function saveMob() {
    const mob = {
        name: mob_name.value,
        level: parseInt(mob_level.value) || 1,
        hp: parseInt(mob_hp.value) || 10,
        damage: parseInt(mob_damage.value) || 1,
        defense: parseInt(mob_defense.value) || 0,

        xp: parseInt(mob_xp.value) || 10,

        gold_min: parseInt(mob_gold_min.value) || 0,
        gold_max: parseInt(mob_gold_max.value) || 0,

        loot: safeJSON(mob_loot.value),
        ai: safeJSON(mob_ai.value),
        flags: safeJSON(mob_flags.value),
        spawn: safeJSON(mob_spawn.value)
    };

    await API.post("/mobs", mob);
    loadMobs();
}

async function deleteMob() {
    if (!state.current.mob) return;
    await API.del("/mobs/" + state.current.mob.name);
    loadMobs();
}