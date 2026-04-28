let rooms = [], currentRoom = null;
let canvas, ctx, wrapper, positions = {}, dragging = null;
let camera = { zoom: 1 };

window.onload = () => {
    canvas = mapCanvas;
    wrapper = mapWrapper;
    ctx = canvas.getContext("2d");
    initCanvas();
    loadRooms();
};

async function loadRooms() {
    let r = await fetch("/rooms");
    rooms = (await r.json()).rooms || [];
    positions = {};

    rooms.forEach((x, i) => {
        positions[x.vnum] = x.pos || { x: 100 + i * 120, y: 100 + i * 80 };
    });

    renderRoomList();
    if (rooms.length) { currentRoom = rooms[0]; loadRoom(currentRoom); }
    drawMap();
}

function renderRoomList() {
    roomList.innerHTML = "";
    rooms.forEach(r => {
        let d = document.createElement("div");
        d.className = "item";
        if (currentRoom && currentRoom.vnum === r.vnum) d.classList.add("active");
        d.innerText = r.vnum + " - " + (r.name || "");
        d.onclick = () => { currentRoom = r; loadRoom(r); renderRoomList(); drawMap(); };
        roomList.appendChild(d);
    });
}

function deleteRoom() {
    if (!currentRoom) return alert("Select room");
    rooms = rooms.filter(r => r.vnum !== currentRoom.vnum);
    saveRooms();
}

function loadRoom(r) {
    room_vnum.value = r.vnum || "";
    room_name.value = r.name || "";
    room_zone.value = r.zone || "";
    room_short.value = r.short_desc || "";
    room_long.value = r.long_desc || "";
    renderExits(r.exits || {});
}

function newRoom() {
    currentRoom = null;
    room_vnum.value = "";
    room_name.value = "";
    room_zone.value = "";
    room_short.value = "";
    room_long.value = "";
    renderExits({});
}

function renderExits(exits) {
    exitsContainer.innerHTML = "";
    ["north", "south", "east", "west", "up", "down"].forEach(dir => {
        let e = exits[dir] || {};
        let d = document.createElement("div");
        d.className = "exit-card";
        d.dataset.dir = dir;

        d.innerHTML = `
<div class="exit-title">${dir}</div>
<div class="exit-row">
<input value="${e.to || ""}">
<input value="${e.key || ""}">
</div>
<div class="exit-flags">
<label><input type="checkbox" ${e.door ? "checked" : ""}>door</label>
<label><input type="checkbox" ${e.closed ? "checked" : ""}>closed</label>
<label><input type="checkbox" ${e.locked ? "checked" : ""}>locked</label>
<label><input type="checkbox" ${e.secret ? "checked" : ""}>secret</label>
</div>`;

        exitsContainer.appendChild(d);
    });
}

function readExits() {
    let res = {};
    [...exitsContainer.children].forEach(c => {
        let i = c.querySelectorAll("input");
        let to = parseInt(i[0].value);
        if (!to) return;
        res[c.dataset.dir] = {
            to,
            key: parseInt(i[1].value) || null,
            door: i[2].checked,
            closed: i[3].checked,
            locked: i[4].checked,
            secret: i[5].checked
        };
    });
    return res;
}

function buildRoom() {
    let v = parseInt(room_vnum.value);
    return {
        vnum: v,
        name: room_name.value,
        short_desc: room_short.value,
        long_desc: room_long.value,
        zone: room_zone.value,
        exits: readExits(),
        pos: positions[v]
    };
}

async function saveRooms() {
    let r = buildRoom();
    let i = rooms.findIndex(x => x.vnum === r.vnum);
    if (i >= 0) rooms[i] = r; else rooms.push(r);

    await fetch("/save_rooms", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ rooms }) });
    loadRooms();
}

function initCanvas() {
    canvas.onmousedown = e => {
        let r = hitNode(e);
        if (r) dragging = r.vnum;
    };

    canvas.onmousemove = e => {
        if (!dragging) return;
        positions[dragging] = getMouseWorld(e);
        drawMap();
    };

    canvas.onmouseup = () => dragging = null;

    canvas.onwheel = e => {
        e.preventDefault();
        camera.zoom = Math.max(0.3, Math.min(2.5, camera.zoom - e.deltaY * 0.001));
        drawMap();
    };
}

function drawMap() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.scale(camera.zoom, camera.zoom);

    rooms.forEach(r => {
        let p = positions[r.vnum];
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
        ctx.beginPath();
        ctx.arc(p.x, p.y, 15, 0, 6.28);
        ctx.fillStyle = "#0ea5e9";
        ctx.fill();
        ctx.fillStyle = "#fff";
        ctx.fillText(r.vnum, p.x - 10, p.y + 4);
    });

    ctx.restore();
}

function getMouseWorld(e) {
    let r = canvas.getBoundingClientRect();
    return {
        x: (e.clientX - r.left + wrapper.scrollLeft) / camera.zoom,
        y: (e.clientY - r.top + wrapper.scrollTop) / camera.zoom
    };
}

function hitNode(e) {
    let m = getMouseWorld(e);
    for (let r of rooms) {
        let p = positions[r.vnum];
        if (Math.hypot(m.x - p.x, m.y - p.y) < 15) return r;
    }
    return null;
}