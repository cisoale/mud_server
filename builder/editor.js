let mobs = [];
let items = [];
let currentMob = null;
let currentItem = null;


// =========================
// SAFE JSON PARSE
// =========================
function safeJSONParse(text, fallback = []) {
    try {
        return JSON.parse(text);
    } catch (e) {
        alert("Errore JSON! Controlla il formato.");
        return fallback;
    }
}


// =========================
// LOAD
// =========================
async function loadData() {
    const mobRes = await fetch("/mobs");
    const itemRes = await fetch("/items");

    mobs = await mobRes.json();
    items = await itemRes.json();

    renderLists();
}


// =========================
// LISTE
// =========================
function renderLists() {

    const mobList = document.getElementById("mobList");
    const itemList = document.getElementById("itemList");

    mobList.innerHTML = "";
    itemList.innerHTML = "";

    mobs.forEach(m => {
        const div = document.createElement("div");
        div.className = "list-item";
        div.innerText = m.name;
        div.onclick = () => loadMob(m);
        mobList.appendChild(div);
    });

    items.forEach(i => {
        const div = document.createElement("div");
        div.className = "list-item";
        div.innerText = i.name;
        div.onclick = () => loadItem(i);
        itemList.appendChild(div);
    });
}


// =========================
// MOB
// =========================
function loadMob(m) {

    currentMob = m || {};

    document.getElementById("mobEditor").style.display = "block";
    document.getElementById("itemEditor").style.display = "none";

    document.getElementById("mob_name").value = m.name || "";
    document.getElementById("mob_desc").value = m.description || "";

    document.getElementById("mob_level").value = m.level || 1;
    document.getElementById("mob_hp").value = m.hp || 10;
    document.getElementById("mob_damage").value = m.damage || 1;
    document.getElementById("mob_defense").value = m.defense || 0;
    document.getElementById("mob_xp").value = m.xp || 10;

    document.getElementById("mob_type").value = m.type || "normal";
    document.getElementById("mob_aggressive").checked = m.aggressive || false;

    document.getElementById("mob_gold_min").value = m.gold_min || 0;
    document.getElementById("mob_gold_max").value = m.gold_max || 0;

    document.getElementById("mob_loot").value =
        JSON.stringify(m.loot || [], null, 2);

    document.getElementById("mob_events").value =
        JSON.stringify(m.death_events || [], null, 2);
}


function saveMob() {

    const mob = {
        name: document.getElementById("mob_name").value,
        description: document.getElementById("mob_desc").value,

        level: +document.getElementById("mob_level").value || 1,
        hp: +document.getElementById("mob_hp").value || 10,
        damage: +document.getElementById("mob_damage").value || 1,
        defense: +document.getElementById("mob_defense").value || 0,
        xp: +document.getElementById("mob_xp").value || 10,

        type: document.getElementById("mob_type").value,
        aggressive: document.getElementById("mob_aggressive").checked,

        gold_min: +document.getElementById("mob_gold_min").value || 0,
        gold_max: +document.getElementById("mob_gold_max").value || 0,

        loot: safeJSONParse(
            document.getElementById("mob_loot").value,
            []
        ),

        death_events: safeJSONParse(
            document.getElementById("mob_events").value,
            []
        ),

        _file: currentMob?._file
    };

    fetch("/save_mob", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(mob)
    });

    alert("Mob salvato!");
}


// =========================
// ITEM
// =========================
function loadItem(i) {

    currentItem = i || {};

    document.getElementById("mobEditor").style.display = "none";
    document.getElementById("itemEditor").style.display = "block";

    document.getElementById("item_name").value = i.name || "";
    document.getElementById("item_desc").value = i.description || "";
    document.getElementById("item_type").value = i.type || "weapon";
    document.getElementById("item_damage").value = i.damage || 0;
    document.getElementById("item_defense").value = i.defense || 0;
    document.getElementById("item_heal").value = i.heal || 0;
    document.getElementById("item_mana").value = i.mana || 0;
    document.getElementById("item_slot").value = i.slot || "weapon";
    document.getElementById("item_rarity").value = i.rarity || "common";
}


function saveItem() {

    const item = {
        name: document.getElementById("item_name").value,
        description: document.getElementById("item_desc").value,
        type: document.getElementById("item_type").value,
        damage: +document.getElementById("item_damage").value || 0,
        defense: +document.getElementById("item_defense").value || 0,
        heal: +document.getElementById("item_heal").value || 0,
        mana: +document.getElementById("item_mana").value || 0,
        slot: document.getElementById("item_slot").value,
        rarity: document.getElementById("item_rarity").value,
        _file: currentItem?._file
    };

    fetch("/save_item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(item)
    });

    alert("Item salvato!");
}


// =========================
// NEW
// =========================
function newMob() {
    loadMob({});
}

function newItem() {
    loadItem({});
}


// =========================
// INIT
// =========================
window.onload = loadData;