window.onload = function () {

    const canvas = document.getElementById("mapCanvas");
    const ctx = canvas.getContext("2d");

    let rooms = [];
    let positions = {};
    let selected = null;

    let isDragging = false;
    let dragOffsetX = 0;
    let dragOffsetY = 0;

    // =========================
    // LOAD ROOMS
    // =========================
    fetch("/rooms")
        .then(res => res.json())
        .then(data => {

            rooms = data;

            let spacingX = 120;
            let spacingY = 100;

            rooms.forEach((r, index) => {

                if (!r.vnum) return;

                if (r.pos && r.pos.x !== undefined) {
                    positions[r.vnum] = r.pos;
                } else {
                    positions[r.vnum] = {
                        x: 50 + (index % 6) * spacingX,
                        y: 50 + Math.floor(index / 6) * spacingY
                    };
                }
            });

            draw();
        });

    // =========================
    // DRAW
    // =========================
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // exits
        rooms.forEach(r => {
            let pos = positions[r.vnum];
            if (!pos) return;

            if (r.exits) {
                for (let dir in r.exits) {

                    let exit = r.exits[dir];
                    let targetPos = positions[exit.to];

                    if (targetPos) {
                        ctx.beginPath();
                        ctx.moveTo(pos.x + 40, pos.y + 20);
                        ctx.lineTo(targetPos.x + 40, targetPos.y + 20);

                        ctx.strokeStyle = exit.secret ? "#444" : "#888";
                        ctx.stroke();
                    }
                }
            }
        });

        // rooms
        rooms.forEach(r => {
            let pos = positions[r.vnum];
            if (!pos) return;

            ctx.fillStyle = (selected == r.vnum) ? "orange" : "lightblue";
            ctx.fillRect(pos.x, pos.y, 80, 40);

            ctx.fillStyle = "black";
            ctx.fillText(r.vnum, pos.x + 5, pos.y + 15);
        });
    }

    // =========================
    // CLICK + DRAG
    // =========================
    canvas.addEventListener("mousedown", e => {

        let rect = canvas.getBoundingClientRect();
        let mx = e.clientX - rect.left;
        let my = e.clientY - rect.top;

        let clicked = null;

        for (let vnum in positions) {
            let p = positions[vnum];

            if (mx > p.x && mx < p.x + 80 &&
                my > p.y && my < p.y + 40) {

                clicked = parseInt(vnum);

                dragOffsetX = mx - p.x;
                dragOffsetY = my - p.y;

                break;
            }
        }

        if (!clicked) return;

        selected = clicked;
        isDragging = true;

        loadRoomInForm(clicked);
        draw();
    });

    canvas.addEventListener("mousemove", e => {

        if (!isDragging || !selected) return;

        let rect = canvas.getBoundingClientRect();
        let mx = e.clientX - rect.left;
        let my = e.clientY - rect.top;

        positions[selected].x = mx - dragOffsetX;
        positions[selected].y = my - dragOffsetY;

        draw();
    });

    canvas.addEventListener("mouseup", () => {

        if (!selected) return;

        isDragging = false;

        let room = rooms.find(r => r.vnum == selected);
        if (!room) return;

        room.pos = positions[selected];

        fetch("/save_room", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(room)
        });
    });

    // =========================
    // LOAD ROOM
    // =========================
    function loadRoomInForm(vnum) {

        let room = rooms.find(r => r.vnum == vnum);
        if (!room) return;

        document.getElementById("vnum").value = room.vnum;
        document.getElementById("name").value = room.name || "";
        document.getElementById("desc").value = room.description || "";

        const dirs = ["north", "south", "east", "west", "up", "down"];

        dirs.forEach(d => {

            let exit = room.exits?.[d];

            if (!exit) {
                document.getElementById("exit_" + d).value = "";
                return;
            }

            document.getElementById("exit_" + d).value = exit.to || "";

            document.getElementById(d + "_door").checked = exit.door || false;
            document.getElementById(d + "_closed").checked = exit.closed || false;
            document.getElementById(d + "_locked").checked = exit.locked || false;
            document.getElementById(d + "_secret").checked = exit.secret || false;

            if (exit.key)
                document.getElementById(d + "_key").value = exit.key;
        });
    }

    // =========================
    // SAVE ROOM (CON PORTE)
    // =========================
    window.saveRoom = function () {

        const dirs = ["north", "south", "east", "west", "up", "down"];
        let exits = {};

        dirs.forEach(d => {

            let to = document.getElementById("exit_" + d).value;
            if (!to) return;

            exits[d] = {
                to: parseInt(to),
                door: document.getElementById(d + "_door")?.checked || false,
                closed: document.getElementById(d + "_closed")?.checked || false,
                locked: document.getElementById(d + "_locked")?.checked || false,
                key: document.getElementById(d + "_key")?.value || null,
                secret: document.getElementById(d + "_secret")?.checked || false
            };
        });

        let vnum = parseInt(document.getElementById("vnum").value);
        let existing = rooms.find(r => r.vnum == vnum);

        const room = {
            vnum: vnum,
            name: document.getElementById("name").value,
            description: document.getElementById("desc").value,
            exits: exits,
            mobs: existing?.mobs || [],
            items: existing?.items || [],
            pos: existing?.pos || { x: 100, y: 100 }
        };

        fetch("/save_room", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(room)
        }).then(() => {

            if (existing) {
                Object.assign(existing, room);
            } else {
                rooms.push(room);
                positions[vnum] = room.pos;
            }

            draw();
            alert("Room salvata!");
        });
    };

};

function loadMobDB() {

    fetch("/mobs")
        .then(res => res.json())
        .then(data => {

            console.log("MOBS:", data);

            let select = document.getElementById("mob_select");
            let list = document.getElementById("mob_db_list");

            if (select) select.innerHTML = "";
            if (list) list.innerHTML = "";

            data.forEach(m => {

                // dropdown
                if (select) {
                    let opt = document.createElement("option");
                    opt.value = m.name;
                    opt.textContent = m.name;
                    select.appendChild(opt);
                }

                // lista editor
                if (list) {
                    let li = document.createElement("li");
                    li.textContent = m.name;

                    li.onclick = () => {
                        document.getElementById("mob_name").value = m.name || "";
                        document.getElementById("mob_hp").value = m.hp || 0;
                        document.getElementById("mob_damage").value = m.damage || 0;
                        document.getElementById("mob_xp").value = m.xp || 0;
                        document.getElementById("mob_loot").value = (m.loot || []).join(",");
                    };

                    list.appendChild(li);
                }

            });

        })
        .catch(err => console.error("Errore mobs:", err));
}

function loadItemDB() {

    fetch("/items")
        .then(res => res.json())
        .then(data => {

            console.log("ITEMS:", data);

            let select = document.getElementById("item_select");
            let list = document.getElementById("item_db_list");

            if (select) select.innerHTML = "";
            if (list) list.innerHTML = "";

            data.forEach(i => {

                // dropdown
                if (select) {
                    let opt = document.createElement("option");
                    opt.value = i.name;
                    opt.textContent = i.name;
                    select.appendChild(opt);
                }

                // lista editor
                if (list) {
                    let li = document.createElement("li");
                    li.textContent = i.name;

                    li.onclick = () => {
                        document.getElementById("item_name").value = i.name || "";
                        document.getElementById("item_type").value = i.type || "";
                        document.getElementById("item_damage").value = i.damage || 0;
                        document.getElementById("item_defense").value = i.defense || 0;
                    };

                    list.appendChild(li);
                }

            });

        })
        .catch(err => console.error("Errore items:", err));
}
loadMobDB();
loadItemDB();