let mobs = [];
let current = null;

document.addEventListener("DOMContentLoaded", () => {
    bindUI();
    load();
});

function bindUI() {
    document.getElementById("saveBtn").onclick = save;
    document.getElementById("newMobBtn").onclick = newMob;
    document.getElementById("addLootBtn").onclick = () => addLoot();

    const delBtn = document.getElementById("deleteBtn");
    if (delBtn) delBtn.onclick = deleteMob;
}

// =========================
// LOAD
// =========================
async function load() {
    const res = await fetch("/mobs");
    mobs = await res.json();
    renderList();
}

function renderList() {
    const list = document.getElementById("mobList");
    list.innerHTML = "";

    mobs.forEach(m => {
        const div = document.createElement("div");
        div.innerText = m.name;
        div.onclick = () => loadMob(m);
        list.appendChild(div);
    });
}

// =========================
// NEW / LOAD
// =========================
function newMob() {
    loadMob({
        name: "",
        description: "",
        type: "normal",
        level: 1,
        hp: 10,
        damage: 1,
        defense: 0,
        xp: 10,
        gold_min: 0,
        gold_max: 0,
        loot: []
    });
}

function loadMob(m) {
    current = m;

    set("name", m.name);
    set("description", m.description);
    set("type", m.type);

    set("level", m.level);
    set("hp", m.hp);
    set("damage", m.damage);
    set("defense", m.defense);
    set("xp", m.xp);

    set("gold_min", m.gold_min);
    set("gold_max", m.gold_max);

    renderLoot(m.loot || []);
}

// =========================
// UTILS
// =========================
function set(id, val) {
    document.getElementById(id).value = val ?? "";
}

function get(id, def = "") {
    return document.getElementById(id).value || def;
}

// =========================
// LOOT
// =========================
function addLoot(data = {}) {
    const div = document.createElement("div");
    div.className = "card";

    div.innerHTML = `
        <input placeholder="item" value="${data.item || ""}">
        <input type="number" step="0.1" placeholder="chance (0-1)" value="${data.chance ?? 0.5}">
        <input type="number" placeholder="min" value="${data.min ?? 1}">
        <input type="number" placeholder="max" value="${data.max ?? 1}">
        <button onclick="this.parentNode.remove()">❌</button>
    `;

    document.getElementById("lootContainer").appendChild(div);
}

function renderLoot(list) {
    const c = document.getElementById("lootContainer");
    c.innerHTML = "";
    list.forEach(addLoot);
}

function getLoot() {
    return [...document.getElementById("lootContainer").children].map(c => ({
        item: c.children[0].value.trim(),
        chance: Math.max(0, Math.min(1, parseFloat(c.children[1].value) || 0)),
        min: Math.max(1, parseInt(c.children[2].value) || 1),
        max: Math.max(1, parseInt(c.children[3].value) || 1)
    }));
}

// =========================
// VALIDATE
// =========================
function validate(m) {
    if (!m.name) return "Nome mancante";
    if (m.hp <= 0) return "HP non valido";

    for (let l of m.loot) {
        if (!l.item) return "Loot senza item";
        if (l.chance < 0 || l.chance > 1) return "Chance non valida";
    }

    return null;
}

// =========================
// SAVE
// =========================
async function save() {

    const mob = {
        name: get("name").trim().toLowerCase().replace(/\s+/g, "_"),
        description: get("description"),
        type: get("type"),

        level: +get("level", 1),
        hp: +get("hp", 10),
        damage: +get("damage", 1),
        defense: +get("defense", 0),
        xp: +get("xp", 10),

        gold_min: +get("gold_min", 0),
        gold_max: +get("gold_max", 0),

        loot: getLoot(),
        _file: current?._file
    };

    const err = validate(mob);

    if (err) {
        alert(err);
        return;
    }

    const res = await fetch("/save_mob", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(mob)
    });

    const data = await res.json();

    if (data.status !== "ok") {
        alert("Errore salvataggio");
        return;
    }

    alert("Mob salvato!");
    load();
}

// =========================
// DELETE
// =========================
async function deleteMob() {

    if (!current || !current._file) {
        alert("Seleziona un mob");
        return;
    }

    if (!confirm("Eliminare questo mob?")) return;

    const res = await fetch("/delete_mob", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ _file: current._file })
    });

    const data = await res.json();

    if (data.status !== "ok") {
        alert("Errore eliminazione");
        return;
    }

    alert("Mob eliminato");
    current = null;
    load();
}