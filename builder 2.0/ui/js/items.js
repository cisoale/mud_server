let currentItem = null;
let items = [];

function $(id) { return document.getElementById(id); }

// LOAD
async function loadItems() {
    const res = await fetch("/items");
    items = await res.json();
    renderItemList();
}

// LIST
function renderItemList() {
    const list = $("itemList");
    list.innerHTML = "";

    items.forEach(i => {
        const div = document.createElement("div");
        div.className = "mob-item";
        div.innerText = i.name;

        if (currentItem && currentItem.name === i.name)
            div.classList.add("active");

        div.onclick = () => {
            currentItem = i;
            loadItem(i);
            renderItemList();
        };

        list.appendChild(div);
    });
}

// LOAD ITEM
function loadItem(i) {
    $("item_name").value = i.name || "";
    $("item_display_name").value = i.display_name || "";
    $("item_type").value = i.type || "misc";
    $("item_value").value = i.value || 10;
}

// NEW
function newItem() {
    currentItem = null;
    $("item_name").value = "";
    $("item_display_name").value = "";
    $("item_type").value = "misc";
    $("item_value").value = 10;
}

// SAVE
async function saveItem() {

    const data = {
        name: $("item_name").value,
        display_name: $("item_display_name").value,
        type: $("item_type").value,
        value: +$("item_value").value
    };

    const res = await fetch("/save_item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (result.status !== "ok") {
        alert("Errore salvataggio");
        return;
    }

    alert("Item salvato");
    loadItems();
}

// DELETE
async function deleteItem() {

    if (!currentItem) return;

    if (!confirm("Eliminare item?")) return;

    await fetch("/delete_item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: currentItem.name })
    });

    currentItem = null;
    loadItems();
}

loadItems();