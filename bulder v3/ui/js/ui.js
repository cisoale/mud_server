function showTab(id) {
    document.querySelectorAll(".tab-content").forEach(t => t.style.display = "none");
    document.getElementById(id).style.display = "block";

    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    event.target.classList.add("active");
}

function setActive(list, name) {
    [...list.children].forEach(el => {
        el.classList.toggle("active", el.innerText === name);
    });
}