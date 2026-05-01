let rooms = [];
let current = null;
let positions = {};

let canvas, ctx;
let dragging = null;

let modal, editingRoom;


// ================= INIT =================

async function init() {
    modal = document.getElementById("modal");

    const data = await API.get("/rooms");
    rooms = data.rooms || [];

    rooms.forEach((r, i) => {
        let v = parseInt(r.vnum);
        if (!v) return;

        positions[v] = r.pos || {
            x: 100 + (i % 10) * 80,
            y: 100 + Math.floor(i / 10) * 80
        };
    });

    renderList();
    initMap();
}


// ================= SIDEBAR =================

function renderList() {
    sidebar.innerHTML = "";

    rooms.forEach(r => {
        let d = document.createElement("div");
        d.innerText = r.vnum;

        d.onclick = () => openModal(r);

        sidebar.appendChild(d);
    });
}


// ================= MODAL =================

function openModal(room) {

    editingRoom = room || {
        vnum: Date.now(),
        name: "",
        long_desc: "",
        exits: {}
    };

    m_vnum.value = editingRoom.vnum || "";
    m_name.value = editingRoom.name || "";
    m_desc.value = editingRoom.long_desc || "";

    renderModalExits(editingRoom.exits);

    modal.style.display = "flex";
}

function closeModal() {
    modal.style.display = "none";
}


function renderModalExits(exits) {

    m_exits.innerHTML = "";

    ["north", "south", "east", "west"].forEach(dir => {

        let e = exits[dir] || {};

        let div = document.createElement("div");

        div.innerHTML = `
            <b>${dir}</b>
            <input placeholder="to" value="${e.to || ""}">
            <label><input type="checkbox" ${e.door ? "checked" : ""}>door</label>
            <label><input type="checkbox" ${e.locked ? "checked" : ""}>locked</label>
            <label><input type="checkbox" ${e.hidden ? "checked" : ""}>hidden</label>
        `;

        div.dataset.dir = dir;

        m_exits.appendChild(div);
    });
}


function readModalExits() {

    let res = {};

    document.querySelectorAll("#m_exits div").forEach(div => {

        let inputs = div.querySelectorAll("input");

        let to = parseInt(inputs[0].value);
        if (!to) return;

        res[div.dataset.dir] = {
            to: to,
            door: inputs[1].checked,
            locked: inputs[2].checked,
            hidden: inputs[3].checked
        };
    });

    return res;
}


async function saveModal() {

    let v = parseInt(m_vnum.value);
    if (!v) return alert("Invalid VNUM");

    editingRoom.vnum = v;
    editingRoom.name = m_name.value;
    editingRoom.long_desc = m_desc.value;
    editingRoom.exits = readModalExits();
    editingRoom.pos = positions[v] || { x: 200, y: 200 };

    await API.post("/rooms", editingRoom);

    closeModal();
    init();
}


// ================= MAP =================

function initMap() {

    canvas = document.getElementById("map");
    ctx = canvas.getContext("2d");

    resize();
    window.onresize = resize;

    canvas.onmousedown = e => {
        dragging = hit(e);
    };

    canvas.onmouseup = async () => {
        if (dragging) {
            let r = rooms.find(x => x.vnum == dragging);
            r.pos = positions[dragging];
            await API.post("/rooms", r);
        }
        dragging = null;
    };

    canvas.onmousemove = e => {
        if (!dragging) return;

        let rect = canvas.getBoundingClientRect();

        let x = e.clientX - rect.left;
        let y = e.clientY - rect.top;

        positions[dragging] = {
            x: Math.round(x / 50) * 50,
            y: Math.round(y / 50) * 50
        };

        draw();
    };

    canvas.ondblclick = e => {
        openModal(); // nuova room
    };

    draw();
}


// ================= DRAW =================

function draw() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawGrid();

    rooms.forEach(r => {
        let p = positions[r.vnum];
        if (!p) return;

        Object.values(r.exits || {}).forEach(e => {
            let t = positions[e.to];
            if (!t) return;

            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(t.x, t.y);
            ctx.strokeStyle = "#334155";
            ctx.stroke();
        });
    });

    rooms.forEach(r => {
        let p = positions[r.vnum];
        if (!p) return;

        ctx.beginPath();
        ctx.arc(p.x, p.y, 12, 0, Math.PI * 2);

        ctx.fillStyle = "#0ea5e9";
        ctx.fill();

        ctx.fillStyle = "#fff";
        ctx.fillText(r.vnum, p.x + 14, p.y + 4);
    });
}


function drawGrid() {
    ctx.strokeStyle = "#1e293b";

    for (let x = 0; x < canvas.width; x += 50) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }

    for (let y = 0; y < canvas.height; y += 50) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}


// ================= UTILS =================

function hit(e) {

    let rect = canvas.getBoundingClientRect();

    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;

    for (let r of rooms) {
        let p = positions[r.vnum];
        if (!p) continue;

        if (Math.hypot(x - p.x, y - p.y) < 12) {
            return r.vnum;
        }
    }
}

function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight - 50;
}