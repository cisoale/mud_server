let rooms = [];
let selectedRoom = null;

const map = document.getElementById("map");
const canvas = document.getElementById("lines");
const ctx = canvas.getContext("2d");

const DIRECTIONS = ["north", "south", "east", "west", "up", "down"];

/* =========================
   LOAD
========================= */
async function loadRooms() {

    const res = await fetch("/rooms");
    const data = await res.json();

    rooms = data.rooms || [];

    render();
}

window.onload = loadRooms;


/* =========================
   RENDER
========================= */
function render() {
    renderRooms();
    drawLines();
}


/* =========================
   ROOMS
========================= */
function renderRooms() {

    map.querySelectorAll(".room").forEach(e => e.remove());

    rooms.forEach(room => {

        const div = document.createElement("div");
        div.className = "room";
        div.innerText = room.vnum;

        div.style.left = (room.x || 100) + "px";
        div.style.top = (room.y || 100) + "px";

        div.onclick = () => selectRoom(room, div);
        div.onmousedown = (e) => startDrag(e, room, div);

        map.appendChild(div);
    });
}

///
function goTo(url) {
    window.location.href = url;
}

/* =========================
   SELECT
========================= */
function selectRoom(room, div) {

    updateRoom();

    selectedRoom = room;

    document.querySelectorAll(".room").forEach(r => r.classList.remove("selected"));
    div.classList.add("selected");

    document.getElementById("roomVnum").value = room.vnum;
    document.getElementById("roomName").value = room.name || "";
    document.getElementById("roomDesc").value = room.description || "";

    renderExits();
}


/* =========================
   UPDATE ROOM
========================= */
function updateRoom() {

    if (!selectedRoom) return;

    selectedRoom.name = document.getElementById("roomName").value;
    selectedRoom.description = document.getElementById("roomDesc").value;
}


/* =========================
   EXITS UI
========================= */
function renderExits() {

    const container = document.getElementById("exits");
    container.innerHTML = "";

    DIRECTIONS.forEach(dir => {

        let exit = selectedRoom.exits?.[dir] || {
            to: "",
            door: false,
            closed: false,
            locked: false,
            secret: false,
            key: ""
        };

        container.innerHTML += `
            <div class="exit-card">

                <div class="exit-header">${dir.toUpperCase()}</div>

                <div class="exit-grid">
                    <input class="exit-input"
                        placeholder="Dest"
                        value="${exit.to || ""}"
                        onchange="updateExit('${dir}','to',this.value)">

                    <input class="exit-input"
                        placeholder="Key"
                        value="${exit.key || ""}"
                        onchange="updateExit('${dir}','key',this.value)">
                </div>

                <div class="exit-flags">
                    ${flag(dir, "door", exit, "🚪")}
                    ${flag(dir, "closed", exit, "❌")}
                    ${flag(dir, "locked", exit, "🔒")}
                    ${flag(dir, "secret", exit, "👁")}
                </div>

            </div>
        `;
    });
}


function flag(dir, key, exit, icon) {
    return `
        <label class="flag ${exit[key] ? "active" : ""}">
            <input type="checkbox"
                ${exit[key] ? "checked" : ""}
                onchange="updateExit('${dir}','${key}',this.checked)">
            ${icon}
        </label>
    `;
}


/* =========================
   UPDATE EXIT
========================= */
function updateExit(dir, key, value) {

    if (!selectedRoom.exits) selectedRoom.exits = {};

    if (!selectedRoom.exits[dir]) {
        selectedRoom.exits[dir] = {
            to: null,
            door: false,
            closed: false,
            locked: false,
            secret: false,
            key: null
        };
    }

    if (key === "to") {
        selectedRoom.exits[dir].to = parseInt(value) || null;
    } else if (key === "key") {
        selectedRoom.exits[dir].key = value || null;
    } else {
        selectedRoom.exits[dir][key] = value;
    }

    drawLines();
}


/* =========================
   DRAW LINES
========================= */
function drawLines() {

    canvas.width = map.clientWidth;
    canvas.height = map.clientHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    rooms.forEach(room => {

        if (!room.exits) return;

        Object.values(room.exits).forEach(exit => {

            if (!exit.to) return;

            const target = rooms.find(r => r.vnum == exit.to);
            if (!target) return;

            const x1 = room.x + 30;
            const y1 = room.y + 30;

            const x2 = target.x + 30;
            const y2 = target.y + 30;

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);

            if (exit.locked) ctx.strokeStyle = "red";
            else if (exit.closed) ctx.strokeStyle = "orange";
            else if (exit.secret) ctx.strokeStyle = "purple";
            else ctx.strokeStyle = "#888";

            ctx.lineWidth = 2;
            ctx.stroke();
        });
    });
}


/* =========================
   SAVE
========================= */
async function saveRooms() {

    updateRoom();

    await fetch("/save_rooms", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rooms })
    });

    alert("Salvato!");
}


/* =========================
   CREATE ROOM
========================= */
map.ondblclick = (e) => {

    const newRoom = {
        vnum: generateVnum(),
        name: "Nuova Room",
        description: "",
        exits: {},
        items: [],
        mobs: [],
        x: e.offsetX,
        y: e.offsetY
    };

    rooms.push(newRoom);
    render();
};


function generateVnum() {
    return Math.max(...rooms.map(r => r.vnum || 1000)) + 1;
}


/* =========================
   DRAG
========================= */
let dragging = null;

function startDrag(e, room, div) {

    dragging = { room, div };

    document.onmousemove = (e) => {

        if (!dragging) return;

        const rect = map.getBoundingClientRect();

        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        room.x = x;
        room.y = y;

        div.style.left = x + "px";
        div.style.top = y + "px";

        drawLines();
    };

    document.onmouseup = () => dragging = null;
}