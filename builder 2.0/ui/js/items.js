let items = [];
let currentItem = null;

async function loadItems() {

    try {
        const res = await fetch("/items");

        if (!res.ok) {
            console.error("Errore HTTP /items", res.status);
            return;
        }

        const data = await res.json();

        console.log("ITEMS:", data);

        // 🔥 SUPPORTA ENTRAMBI I FORMATI
        items = Array.isArray(data) ? data : (data.items || []);

        renderItems();

    } catch (err) {
        console.error("Errore loadItems:", err);
    }
}

function renderItems() {

    const list = document.getElementById("itemList");
    if (!list) return;

    list.innerHTML = "";

    items.forEach(i => {

        const div = document.createElement("div");
        div.className = "item";
        div.innerText = i.name || "NO_NAME";

        if (currentItem && currentItem.name === i.name) {
            div.style.background = "#1e293b";
        }

        div.onclick = () => {
            currentItem = i;
            loadItem(i);
            renderItems();
        };

        list.appendChild(div);
    });
}

function loadItem(i) {

    item_name.value = i.name || "";
    item_display_name.value = i.display_name || "";
    item_type.value = i.type || "misc";

    item_value.value = i.value || 0;
    item_weight.value = i.weight || 0;

    item_slot.value = i.slot || "";
    item_defense.value = i.defense || 0;
    item_damage.value = i.damage || 0;
}

function newItem() {
    currentItem = null;
    item_name.value = "";
    item_display_name.value = "";
}

function deleteItem() {

    if (!currentItem) return alert("Seleziona un item");

    if (!confirm("Eliminare item?")) return;

    items = items.filter(i => i.name !== currentItem.name);
    currentItem = null;

    saveItem();
}

async function saveItem() {

    const item = {
        name: item_name.value,
        display_name: item_display_name.value,
        type: item_type.value,

        value: parseInt(item_value.value) || 0,
        weight: parseInt(item_weight.value) || 0,

        slot: item_slot.value,
        defense: parseInt(item_defense.value) || 0,
        damage: parseInt(item_damage.value) || 0,

        rarity: "common",
        stackable: false,
        effects: {}
    };

    const idx = items.findIndex(i => i.name === item.name);

    if (idx >= 0) items[idx] = item;
    else items.push(item);

    await fetch("/save_items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items })
    });

    loadItems();
}