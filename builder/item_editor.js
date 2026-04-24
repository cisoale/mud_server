let items = [];
let current = null;

// =========================
// LOAD
// =========================
async function load() {
    const res = await fetch("/items");
    items = await res.json();
    render();
}

function render() {
    const list = document.getElementById("itemList");
    list.innerHTML = "";

    items.forEach(i => {
        const div = document.createElement("div");
        div.innerText = i.name;
        div.onclick = () => loadItem(i);
        list.appendChild(div);
    });
}

// =========================
// NEW / LOAD
// =========================
function newItem() {
    loadItem({
        name: "",
        type: "misc",
        rarity: "common"
    });
}

function loadItem(i) {
    current = i;

    set("name", i.name);
    set("display_name", i.display_name);
    set("description", i.description);

    set("type", i.type);
    set("rarity", i.rarity);

    set("value", i.value);
    set("weight", i.weight);

    set("damage", i.damage);
    set("defense", i.defense);

    if (i.consumable) {
        set("heal", i.consumable.heal);
        set("mana", i.consumable.mana);
    }

    updateType();
}

// =========================
// UTILS
// =========================
function set(id, val) {
    document.getElementById(id).value = val ?? "";
}

function get(id, def = 0) {
    return document.getElementById(id).value || def;
}

// =========================
// TYPE SWITCH
// =========================
function updateType() {
    const t = get("type");

    document.getElementById("weaponFields").style.display = t === "weapon" ? "block" : "none";
    document.getElementById("armorFields").style.display = t === "armor" ? "block" : "none";
    document.getElementById("consumableFields").style.display = t === "consumable" ? "block" : "none";
}

// =========================
// VALIDATE
// =========================
function validate(data) {
    if (!data.name) return "Nome mancante";
    if (data.name.includes(" ")) return "Usa snake_case";
    return null;
}

// =========================
// SAVE
// =========================
async function save() {

    const data = {
        name: get("name").trim().toLowerCase().replace(/\s+/g, "_"),
        display_name: get("display_name"),
        description: get("description"),
        type: get("type"),
        rarity: get("rarity"),
        value: +get("value", 10),
        weight: +get("weight", 1)
    };

    if (data.type === "weapon") {
        data.damage = +get("damage", 1);
        data.slot = "weapon";
    }

    if (data.type === "armor") {
        data.defense = +get("defense", 1);
        data.slot = get("slot");
    }

    if (data.type === "consumable") {
        data.consumable = {
            heal: +get("heal", 0),
            mana: +get("mana", 0)
        };
    }

    const err = validate(data);

    if (err) {
        alert(err);
        return;
    }

    await fetch("/save_item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    alert("Item salvato!");
    load();
}

// =========================
// DELETE
// =========================
async function deleteItem() {

    if (!current || !current.name) {
        alert("Seleziona un item");
        return;
    }

    if (!confirm("Eliminare questo item?")) return;

    const res = await fetch("/delete_item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: current.name })
    });

    const data = await res.json();

    if (data.status !== "ok") {
        alert("Errore eliminazione");
        return;
    }

    alert("Item eliminato");
    current = null;
    load();
}

load();