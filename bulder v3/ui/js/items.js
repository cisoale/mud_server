async function loadItems() {
    const data = await API.get("/items");
    state.items = data.items || [];
    renderItems();
}

function renderItems() {
    itemList.innerHTML = "";

    state.items.forEach(i => {
        let d = document.createElement("div");
        d.className = "item";
        d.innerText = i.name;

        d.onclick = () => {
            state.current.item = i;
            title.innerText = i.name;

            item_name.value = i.name || "";
            item_display_name.value = i.display_name || "";
        };

        itemList.appendChild(d);
    });
}