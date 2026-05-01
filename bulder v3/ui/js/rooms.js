let rooms = [];
let current = null;

let positions = {};

let canvas, ctx;

console.log("ROOMS JS LOADED");
// ================= INIT =================

async function init() {
    console.log("ROOM BUILDER INIT");

    const data = await API.get("/rooms");

    rooms = data.rooms || [];

    // posizioni base
    rooms.forEach((r, i) => {
        let v = parseInt(r.vnum);
        if (!v) return;

        positions[v] = r.pos || { x: 100 + i * 60, y: 100 };
    });

    renderList();
    initMap();
}


// ================= LIST =================

function renderList() {
    const list = document.getElementById("list");
    list.innerHTML = "";

    rooms.forEach(r => {
        let d = document.createElement("div");
        d.innerText = r.vnum;

        d.onclick = () => {
            selectRoom(r);
        };

        list.appendChild(d);
    });
}


// ================= SELECT =================

function selectRoom(r) {
    current = r;

    document.getElementById("title").innerText = r.vnum;

    vnum.value = r.vnum || "";
    name.value = r.name || "";
    desc.value = r.long_desc || "";

    draw();
}


// ================= SAVE =================

async function saveRoom() {

    if (!current) {
        alert("No room selected");
        return;
    }

    current.name = name.value;
    current.long_desc = desc.value;

    let v = parseInt(vnum.value);

    if (!v) {
        alert("Invalid VNUM");
        return;
    }

    current.vnum = v;
    current.pos = positions[v];

    await API.post("/rooms", current);

    alert("Saved");
}


// ================= MAP =================

function initMap() {

    canvas = document.getElementById("map");
    ctx = canvas.getContext("2d");

    canvas.onmousedown = e => {
        let hit = hitNode(e);
        if (hit) {
            current = rooms.find(r => r.vnum == hit);
        }
    };

    canvas.onmousemove = e => {
        if (!current) return;

        let rect = canvas.getBoundingClientRect();

        let x = e.clientX - rect.left;
        let y = e.clientY - rect.top;

        positions[current.vnum] = { x, y };

        draw();
    };

    draw();
}


function draw() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // links
    rooms.forEach(r => {
        let p = positions[r.vnum];

        if (!p) return;

        Object.values(r.exits || {}).forEach(e => {
            let t = positions[e.to];
            if (!t) return;

            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(t.x, t.y);
            ctx.stroke();
        });
    });

    // nodes
    rooms.forEach(r => {
        let p = positions[r.vnum];
        if (!p) return;

        ctx.beginPath();
        ctx.arc(p.x, p.y, 10, 0, Math.PI * 2);

        ctx.fillStyle = (current && current.vnum == r.vnum) ? "green" : "blue";
        ctx.fill();

        ctx.fillText(r.vnum, p.x + 12, p.y);
    });
}


// ================= UTILS =================

function hitNode(e) {

    let rect = canvas.getBoundingClientRect();

    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;

    for (let r of rooms) {
        let p = positions[r.vnum];
        if (!p) continue;

        if (Math.hypot(x - p.x, y - p.y) < 10) {
            return r.vnum;
        }
    }
}