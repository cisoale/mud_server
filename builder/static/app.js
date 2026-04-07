window.onload = function () {

    const canvas = document.getElementById("mapCanvas");
    const ctx = canvas.getContext("2d");

    let rooms = [];
    let positions = {};
    let selected = null;

    let linkMode = false;
    let linkSource = null;

    // =========================
    // 📦 CARICA ROOM
    // =========================
    fetch("/rooms")
        .then(res => res.json())
        .then(data => {
            console.log("ROOMS:", data);

            rooms = data;

            let x = 50, y = 50;

            rooms.forEach(r => {
                if (r.pos) {
                    positions[r.vnum] = r.pos;
                } else {
                    positions[r.vnum] = { x, y };

                    x += 150;
                    if (x > 700) {
                        x = 50;
                        y += 150;
                    }
                }
            });

            draw();
        })
        .catch(err => console.error("Errore caricamento rooms:", err));


    // =========================
    // 🎨 DRAW MAP
    // =========================
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 🔗 collegamenti
        rooms.forEach(r => {
            let pos = positions[r.vnum];
            if (!pos) return;

            for (let dir in (r.exits || {})) {
                let target = r.exits[dir];
                let targetPos = positions[target];

                if (targetPos) {
                    ctx.beginPath();
                    ctx.moveTo(pos.x + 40, pos.y + 20);
                    ctx.lineTo(targetPos.x + 40, targetPos.y + 20);
                    ctx.stroke();
                }
            }
        });

        // 🟦 room
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
    // 🖱️ CLICK / LINK MODE
    // =========================
    canvas.addEventListener("mousedown", e => {
        let rect = canvas.getBoundingClientRect();
        let mx = e.clientX - rect.left;
        let my = e.clientY - rect.top;

        let clicked = null;

        for (let vnum in positions) {
            let p = positions[vnum];

            if (
                mx > p.x && mx < p.x + 80 &&
                my > p.y && my < p.y + 40
            ) {
                clicked = vnum;
                break;
            }
        }

        if (!clicked) return;

        // 🔗 LINK MODE
        if (linkMode) {
            if (!linkSource) {
                linkSource = clicked;
                alert("Seleziona destinazione");
            } else {
                createLink(linkSource, clicked);
                linkSource = null;
            }
            return;
        }

        selected = clicked;
        draw();
    });


    // =========================
    // 🖱️ DRAG
    // =========================
    canvas.addEventListener("mousemove", e => {
        if (!selected) return;

        let rect = canvas.getBoundingClientRect();

        positions[selected].x = e.clientX - rect.left;
        positions[selected].y = e.clientY - rect.top;

        draw();
    });


    canvas.addEventListener("mouseup", () => {
        if (selected) {
            savePosition(selected);
        }
        selected = null;
    });


    // =========================
    // 💾 SALVA POSIZIONE
    // =========================
    function savePosition(vnum) {
        let room = rooms.find(r => r.vnum == vnum);
        if (!room) return;

        room.pos = positions[vnum];

        fetch("/save_room", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(room)
        })
        .then(res => res.json())
        .then(() => console.log("Posizione salvata"))
        .catch(err => console.error(err));
    }


    // =========================
    // 🔗 CREA LINK
    // =========================
    function createLink(from, to) {
        let room = rooms.find(r => r.vnum == from);
        if (!room) return;

        if (!room.exits) room.exits = {};

        let dir = prompt("Direzione? (north/south/east/west/up/down)");
        if (!dir) return;

        room.exits[dir] = parseInt(to);

        fetch("/save_room", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(room)
        })
        .then(res => res.json())
        .then(() => {
            alert("Collegamento creato!");
            draw();
        })
        .catch(err => console.error(err));
    }


    // =========================
    // 💾 SALVA ROOM DA FORM
    // =========================
    window.saveRoom = function () {
        try {
            const room = {
                vnum: parseInt(document.getElementById("vnum").value),
                name: document.getElementById("name").value,
                description: document.getElementById("desc").value,
                exits: JSON.parse(document.getElementById("exits").value || "{}")
            };

            fetch("/save_room", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(room)
            })
            .then(res => res.json())
            .then(data => {
                console.log("SALVATO:", data);
                alert("Room salvata!");

                rooms.push(room);
                positions[room.vnum] = { x: 100, y: 100 };

                draw();
            })
            .catch(err => {
                console.error(err);
                alert("Errore salvataggio!");
            });

        } catch (e) {
            alert("Errore nei dati (JSON exits?)");
            console.error(e);
        }
    };


    // =========================
    // 🔘 TOGGLE LINK MODE
    // =========================
    window.toggleLinkMode = function () {
        linkMode = !linkMode;
        linkSource = null;
        alert("Link mode: " + (linkMode ? "ON" : "OFF"));
    };

};