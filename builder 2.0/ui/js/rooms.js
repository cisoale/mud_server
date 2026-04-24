// =========================
// STATE
// =========================
let rooms = [];
let currentRoom = null;

let canvas, ctx;
let positions = {}; // vnum -> {x,y}
let dragging = null;

// =========================
// UTILS
// =========================
function $(id) { return document.getElementById(id); }

function setVal(id, value) {
    const el = $(id);
    if (el) el.value = value ?? "";
}

function getVal(id) {
    const el = $(id);
    return el ? el.value : "";
}

// =========================
// INIT
// =========================
window.addEventListener("load", () => {
    initCanvas();
    loadRooms();
});

// =========================
// LOAD ROOMS
// =========================
async function loadRooms() {

    const res = await fetch("/rooms");
    const data = await res.json();

    rooms = data.rooms || [];

    // assegna posizione se manca
    rooms.forEach(r => {
        if (!positions[r.vnum]) {
            positions[r.vnum] = {
                x: Math.random() * 700 + 80,
                y: Math.random() * 400 + 80
            };
        }
    });

    renderRoomList();

    if (rooms.length > 0) {
        currentRoom = rooms[0];
        loadRoom(currentRoom);
    }

    drawMap();
}

// =========================
// LIST
// =========================
function renderRoomList() {

    const list = $("roomList");
    if (!list) return;

    list.innerHTML = "";

    rooms.forEach(r => {

        const div = document.createElement("div");
        div.className = "mob-item";
        div.innerText = `${r.vnum} - ${r.name || ""}`;

        if (currentRoom && currentRoom.vnum === r.vnum)
            div.classList.add("active");

        div.onclick = () => {
            currentRoom = r;
            loadRoom(r);
            renderRoomList();
            drawMap();
        };

        list.appendChild(div);
    });
}

// =========================
// LOAD ROOM
// =========================
function loadRoom(r) {

    if (!r) return;

    setVal("room_vnum", r.vnum);
    setVal("room_name", r.name);
    setVal("room_zone", r.zone);

    setVal("room_short", r.short_desc);
    setVal("room_long", r.long_desc);

    // exits sempre renderizzati
    renderExits(r.exits || {});
}

// =========================
// NEW ROOM
// =========================
function newRoom() {

    currentRoom = null;

    setVal("room_vnum", "");
    setVal("room_name", "");
    setVal("room_zone", "");

    setVal("room_short", "");
    setVal("room_long", "");

    renderExits({});
}

// =========================
// EXITS UI
// =========================
function renderExits(exits) {

    const container = $("exitsContainer");
    if (!container) return;

    container.innerHTML = "";

    const dirs = ["north", "south", "east", "west", "up", "down"];

    dirs.forEach(dir => {

        const e = exits[dir] || {};

        const div = document.createElement("div");
        div.className = "exit-card";
        div.dataset.dir = dir;

        div.innerHTML = `
            <div class="exit-title">${dir.toUpperCase()}</div>
            <div class="exit-row">
                <input type="number" placeholder="to" value="${e.to || ""}">

                <label><input type="checkbox" ${e.door ? "checked" : ""}>door</label>
                <label><input type="checkbox" ${e.closed ? "checked" : ""}>closed</label>
                <label><input type="checkbox" ${e.locked ? "checked" : ""}>locked</label>

                <input type="number" placeholder="key" value="${e.key || ""}">

                <label><input type="checkbox" ${e.secret ? "checked" : ""}>secret</label>
            </div>
        `;

        container.appendChild(div);
    });
}

// =========================
// READ EXITS
// =========================
function readExits() {

    const res = {};
    const container = $("exitsContainer");

    if (!container) return res;

    [...container.children].forEach(card => {

        const dir = card.dataset.dir;
        const row = card.querySelector(".exit-row").children;

        const to = parseInt(row[0].value) || null;

        if (!to) return;

        res[dir] = {
            to: to,
            door: row[1].firstChild.checked,
            closed: row[2].firstChild.checked,
            locked: row[3].firstChild.checked,
            key: parseInt(row[4].value) || null,
            secret: row[5].firstChild.checked
        };
    });

    return res;
}

// =========================
// BUILD ROOM
// =========================
function buildRoom() {

    const vnum = parseInt(getVal("room_vnum"));

    return {
        vnum: vnum,
        name: getVal("room_name"),
        short_desc: getVal("room_short"),
        long_desc: getVal("room_long"),
        zone: getVal("room_zone"),
        exits: readExits()
    };
}

// =========================
// SAVE
// =========================
async function saveRooms() {

    const room = buildRoom();

    if (!room.vnum) {
        alert("Inserisci VNUM valido");
        return;
    }

    const idx = rooms.findIndex(r => r.vnum === room.vnum);

    if (idx >= 0) {
        rooms[idx] = room;
    } else {
        rooms.push(room);
    }

    const res = await fetch("/save_rooms", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rooms: rooms })
    });

    const result = await res.json();

    if (result.status !== "ok") {
        alert("Errore salvataggio");
        return;
    }

    alert("Room salvata!");

    await loadRooms();

    currentRoom = rooms.find(r => r.vnum === room.vnum);

    renderRoomList();
    loadRoom(currentRoom);
    drawMap();
}

// =========================
// CANVAS
// =========================
function initCanvas() {

    canvas = $("mapCanvas");
    if (!canvas) return;

    ctx = canvas.getContext("2d");

    canvas.addEventListener("mousedown", e => {
        const r = hitNode(e);
        if (r) dragging = r.vnum;
    });

    canvas.addEventListener("mousemove", e => {
        if (!dragging) return;

        const pos = getMouse(e);
        positions[dragging] = pos;

        drawMap();
    });

    canvas.addEventListener("mouseup", () => dragging = null);
    canvas.addEventListener("mouseleave", () => dragging = null);

    canvas.addEventListener("click", e => {
        const r = hitNode(e);
        if (!r) return;

        currentRoom = r;
        loadRoom(r);
        renderRoomList();
        drawMap();
    });
}

// =========================
// MAP DRAW
// =========================
function drawMap() {

    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // linee
    rooms.forEach(r => {
        const p = positions[r.vnum];
        if (!p) return;

        const exits = r.exits || {};

        Object.values(exits).forEach(e => {
            if (!e || !e.to) return;

            const t = positions[e.to];
            if (!t) return;

            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(t.x, t.y);
            ctx.strokeStyle = "#334155";
            ctx.stroke();
        });
    });

    // nodi
    rooms.forEach(r => {
        const p = positions[r.vnum];
        if (!p) return;

        ctx.beginPath();
        ctx.arc(p.x, p.y, 16, 0, Math.PI * 2);
        ctx.fillStyle = (currentRoom && currentRoom.vnum === r.vnum)
            ? "#facc15"
            : "#0ea5e9";
        ctx.fill();

        ctx.fillStyle = "#fff";
        ctx.font = "11px Arial";
        ctx.fillText(r.vnum, p.x - 10, p.y + 4);
    });
}

// =========================
// HELPERS MAP
// =========================
function getMouse(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
}

function hitNode(e) {
    const m = getMouse(e);

    for (let r of rooms) {
        const p = positions[r.vnum];
        if (!p) continue;

        const dx = m.x - p.x;
        const dy = m.y - p.y;

        if (Math.sqrt(dx * dx + dy * dy) < 16)
            return r;
    }

    return null;
}