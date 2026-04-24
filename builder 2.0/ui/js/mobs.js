let currentMob = null;
let mobs = [];

function $(id) { return document.getElementById(id); }

// LOAD
async function loadMobs() {
    const res = await fetch("/mobs");
    mobs = await res.json();
    renderMobList();
}

// LIST
function renderMobList() {
    const list = $("mobList");
    list.innerHTML = "";

    mobs.forEach(m => {
        const div = document.createElement("div");
        div.className = "mob-item";
        div.innerText = m.name;

        if (currentMob && currentMob._file === m._file)
            div.classList.add("active");

        div.onclick = () => {
            currentMob = m;
            loadMob(m);
            renderMobList();
        };

        list.appendChild(div);
    });
}

// LOAD MOB
function loadMob(m) {
    $("mob_name").value = m.name || "";
    $("mob_hp").value = m.hp || 10;
    $("mob_damage").value = m.damage || 1;
    $("mob_xp").value = m.xp || 10;

    renderLoot(m.loot || []);
}

// NEW
function newMob() {
    currentMob = null;
    $("mob_name").value = "";
    $("mob_hp").value = 10;
    $("mob_damage").value = 1;
    $("mob_xp").value = 10;
    $("mob_loot").innerHTML = "";
}

// LOOT
function addLoot(data = {}) {
    const row = document.createElement("div");
    row.className = "loot-row";

    row.innerHTML = `
        <input placeholder="item" value="${data.item || ""}">
        <input type="number" step="0.1" value="${data.chance || 0.5}">
        <button onclick="this.parentNode.remove()">x</button>
    `;

    $("mob_loot").appendChild(row);
}

function renderLoot(list) {
    $("mob_loot").innerHTML = "";
    list.forEach(addLoot);
}

function getLoot() {
    return [...$("mob_loot").children].map(r => ({
        item: r.children[0].value,
        chance: parseFloat(r.children[1].value) || 0
    }));
}

// SAVE
async function saveMob() {

    const data = {
        name: $("mob_name").value,
        hp: +$("mob_hp").value,
        damage: +$("mob_damage").value,
        xp: +$("mob_xp").value,
        loot: getLoot(),
        _file: currentMob?._file
    };

    const res = await fetch("/save_mob", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (result.status !== "ok") {
        alert("Errore salvataggio");
        return;
    }

    alert("Mob salvato");
    loadMobs();
}

// DELETE
async function deleteMob() {

    if (!currentMob) return;

    if (!confirm("Eliminare mob?")) return;

    await fetch("/delete_mob", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ _file: currentMob._file })
    });

    currentMob = null;
    loadMobs();
}

loadMobs();