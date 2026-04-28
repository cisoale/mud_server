let mobs = [];
let currentMob = null;

async function loadMobs() {

    try {
        const res = await fetch("/mobs");

        if (!res.ok) {
            console.error("Errore HTTP /mobs", res.status);
            return;
        }

        const data = await res.json();

        console.log("MOBS:", data);

        mobs = Array.isArray(data) ? data : (data.mobs || []);

        renderMobs();

    } catch (err) {
        console.error("Errore loadMobs:", err);
    }
}

function renderMobs() {

    const list = document.getElementById("mobList");
    if (!list) return;

    list.innerHTML = "";

    mobs.forEach(m => {

        const div = document.createElement("div");
        div.className = "item";
        div.innerText = m.name || "NO_NAME";

        if (currentMob && currentMob.name === m.name) {
            div.style.background = "#1e293b";
        }

        div.onclick = () => {
            currentMob = m;
            loadMob(m);
            renderMobs();
        };

        list.appendChild(div);
    });
}

function loadMob(m) {
    mob_name.value = m.name || "";
    mob_hp.value = m.hp || "";
    mob_damage.value = m.damage || "";
}

function newMob() {
    currentMob = null;
    mob_name.value = "";
    mob_hp.value = "";
    mob_damage.value = "";
}

function deleteMob() {

    if (!currentMob) return alert("Seleziona un mob");

    if (!confirm("Eliminare mob?")) return;

    mobs = mobs.filter(m => m.name !== currentMob.name);
    currentMob = null;

    saveMob();
}

async function saveMob() {

    const mob = {
        name: mob_name.value,
        hp: parseInt(mob_hp.value) || 10,
        damage: parseInt(mob_damage.value) || 1
    };

    const idx = mobs.findIndex(m => m.name === mob.name);

    if (idx >= 0) mobs[idx] = mob;
    else mobs.push(mob);

    await fetch("/save_mobs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobs })
    });

    loadMobs();
}