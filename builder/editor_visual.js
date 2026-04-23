let mobs = [];
let current = null;

document.addEventListener("DOMContentLoaded", () => {
    bindUI();
    load();
});

function bindUI() {
    document.getElementById("saveBtn").addEventListener("click", save);
    document.getElementById("newMobBtn").addEventListener("click", newMob);
    document.getElementById("addLootBtn").addEventListener("click", () => addLoot());
    document.getElementById("addEventBtn").addEventListener("click", () => addEvent());
}

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

function newMob() {
    loadMob({
        name: "mob_" + Date.now(),
        description: "",
        type: "normal",
        level: 1,
        hp: 10,
        damage: 1,
        defense: 0,
        xp: 10,
        gold_min: 0,
        gold_max: 0,
        loot: [],
        death_events: []
    });
}

function loadMob(m) {
    current = m;

    setVal("name", m.name);
    setVal("description", m.description);
    setVal("type", m.type || "normal");

    setVal("level", m.level);
    setVal("hp", m.hp);
    setVal("damage", m.damage);
    setVal("defense", m.defense);
    setVal("xp", m.xp);

    setVal("gold_min", m.gold_min);
    setVal("gold_max", m.gold_max);

    renderLoot(m.loot || []);
    renderEvents(m.death_events || []);
}

function setVal(id, val) {
    document.getElementById(id).value = val ?? "";
}

function getVal(id, fallback = "") {
    return document.getElementById(id).value || fallback;
}

// ===== LOOT =====
function addLoot(data = {}) {
    const div = document.createElement("div");
    div.className = "card";

    div.innerHTML = `
        <input placeholder="Item" value="${data.item || ""}">
        <input type="number" value="${data.chance || 50}">
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
        item: c.children[0].value,
        chance: +c.children[1].value || 0
    }));
}

// ===== EVENTS =====
function addEvent(data = {}) {
    const div = document.createElement("div");
    div.className = "card";

    div.innerHTML = `
        <select>
            <option value="message">Messaggio</option>
            <option value="spawn">Spawn</option>
        </select>
        <input value="${data.text || ""}">
        <input type="number" step="0.1" value="${data.chance || 1}">
        <button onclick="this.parentNode.remove()">❌</button>
    `;

    document.getElementById("eventsContainer").appendChild(div);

    if (data.type) div.children[0].value = data.type;
}

function renderEvents(list) {
    const c = document.getElementById("eventsContainer");
    c.innerHTML = "";
    list.forEach(addEvent);
}

function getEvents() {
    return [...document.getElementById("eventsContainer").children].map(c => ({
        type: c.children[0].value,
        text: c.children[1].value,
        chance: +c.children[2].value || 1
    }));
}

// ===== SAVE =====
async function save() {

    const mob = {
        name: getVal("name").trim().toLowerCase().replace(/\s+/g, "_"),
        description: getVal("description"),
        type: getVal("type", "normal"),

        level: +getVal("level", 1),
        hp: +getVal("hp", 10),
        damage: +getVal("damage", 1),
        defense: +getVal("defense", 0),
        xp: +getVal("xp", 10),

        gold_min: +getVal("gold_min", 0),
        gold_max: +getVal("gold_max", 0),

        loot: getLoot(),
        death_events: getEvents(),

        _file: current?._file
    };

    if (!mob.name) {
        alert("Nome obbligatorio");
        return;
    }

    if (mob.gold_min > mob.gold_max) {
        mob.gold_max = mob.gold_min;
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