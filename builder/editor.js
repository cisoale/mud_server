let mobs = [];
let items = [];
let currentMob = null;
let currentItem = null;


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
    currentMob = m;

    document.getElementById("mobEditor").style.display = "block";
    document.getElementById("itemEditor").style.display = "none";

    document.getElementById("mob_name").value = m.name;
    document.getElementById("mob_desc").value = m.description;
    document.getElementById("mob_level").value = m.level;
    document.getElementById("mob_hp").value = m.hp;
    document.getElementById("mob_damage").value = m.damage;
    document.getElementById("mob_defense").value = m.defense;
    document.getElementById("mob_xp").value = m.xp;
    document.getElementById("mob_type").value = m.type;
    document.getElementById("mob_aggressive").checked = m.aggressive;
    document.getElementById("mob_loot").value = JSON.stringify(m.loot || []);
}


function saveMob() {

    const mob = {
        name: document.getElementById("mob_name").value,
        description: document.getElementById("mob_desc").value,
        level: +document.getElementById("mob_level").value,
        hp: +document.getElementById("mob_hp").value,
        damage: +document.getElementById("mob_damage").value,
        defense: +document.getElementById("mob_defense").value,
        xp: +document.getElementById("mob_xp").value,
        type: document.getElementById("mob_type").value,
        aggressive: document.getElementById("mob_aggressive").checked,
        loot: JSON.parse(document.getElementById("mob_loot").value || "[]")
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

    currentItem = i;

    document.getElementById("mobEditor").style.display = "none";
    document.getElementById("itemEditor").style.display = "block";

    document.getElementById("item_name").value = i.name;
    document.getElementById("item_desc").value = i.description;
    document.getElementById("item_type").value = i.type;
    document.getElementById("item_damage").value = i.damage;
    document.getElementById("item_defense").value = i.defense;
    document.getElementById("item_heal").value = i.heal;
    document.getElementById("item_mana").value = i.mana;
    document.getElementById("item_slot").value = i.slot;
    document.getElementById("item_rarity").value = i.rarity;
}


function saveItem() {

    const item = {
        name: document.getElementById("item_name").value,
        description: document.getElementById("item_desc").value,
        type: document.getElementById("item_type").value,
        damage: +document.getElementById("item_damage").value,
        defense: +document.getElementById("item_defense").value,
        heal: +document.getElementById("item_heal").value,
        mana: +document.getElementById("item_mana").value,
        slot: document.getElementById("item_slot").value,
        rarity: document.getElementById("item_rarity").value
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