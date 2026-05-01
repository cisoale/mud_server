import { state } from "./state.js";

export async function loadItems() {
    const data = await API.get("/items");
    state.items = data.items;
    renderItems();
}

function renderItems() {
    itemList.innerHTML = "";

    state.items.forEach(i => {
        const div = document.createElement("div");
        div.className = "item";
        div.innerText = i.name;

        div.onclick = () => {
            state.current.item = i;
            loadItem(i);
        };

        itemList.appendChild(div);
    });
}

function loadItem(i) {
    item_name.value = i.name;
    item_display_name.value = i.display_name;
}

export async function saveItem() {
    const item = {
        name: item_name.value,
        display_name: item_display_name.value
    };

    await API.post("/items", item);
    loadItems();
}

export async function deleteItem() {
    const name = state.current.item?.name;
    if (!name) return;

    await API.del(`/items/${name}`);
    loadItems();
}