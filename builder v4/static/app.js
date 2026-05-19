// ========================================
// REALM BUILDER - APP.JS
// PROFESSIONAL EDITOR CORE
// ========================================


// ========================================
// APP STATE
// ========================================

const AppState = {

    rooms: [],

    mobs: [],

    selectedRoom: null,

    selectedMob: null,

    currentEditor: null,

    gridEnabled: true,

    zoom: 1,

    offsetX: 0,

    offsetY: 0
}


// ========================================
// CANVAS
// ========================================

const canvas =
    document.getElementById('mapCanvas')

const ctx =
    canvas.getContext('2d')


// ========================================
// DATA MANAGER
// ========================================

const DataManager = {

    // ====================
    // LOAD ROOMS
    // ====================

    async loadRooms() {

        try {

            const response =
                await fetch('/api/rooms')

            const data =
                await response.json()

            if (Array.isArray(data)) {

                AppState.rooms = data

            } else {

                AppState.rooms =
                    Object.values(data)
            }

            SidebarManager.renderRooms()

            MapRenderer.render()

        } catch (error) {

            console.error(
                'ROOM LOAD ERROR:',
                error
            )
        }
    },


    // ====================
    // LOAD MOBS
    // ====================

    async loadMobs() {

        try {

            const response =
                await fetch('/api/mobs')

            const data =
                await response.json()

            if (Array.isArray(data)) {

                AppState.mobs = data

            } else {

                AppState.mobs =
                    Object.values(data)
            }

            SidebarManager.renderMobs()

        } catch (error) {

            console.error(
                'MOB LOAD ERROR:',
                error
            )
        }
    },


    // ====================
    // SAVE ROOM
    // ====================

    async saveRoom(room) {

        try {

            await fetch('/api/room', {

                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify(room)
            })

            await this.loadRooms()

        } catch (error) {

            console.error(
                'ROOM SAVE ERROR:',
                error
            )
        }
    },


    // ====================
    // SAVE MOB
    // ====================

    async saveMob(mob) {

        try {

            await fetch('/api/mob', {

                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify(mob)
            })

            await this.loadMobs()

        } catch (error) {

            console.error(
                'MOB SAVE ERROR:',
                error
            )
        }
    }
}


// ========================================
// SIDEBAR MANAGER
// ========================================

const SidebarManager = {

    // ====================
    // ROOMS
    // ====================

    renderRooms() {

        const container =
            document.getElementById('rooms')

        container.innerHTML = ''

        AppState.rooms.forEach(room => {

            const entry =
                document.createElement('div')

            entry.className =
                'entry'

            entry.innerText =
                `${room.vnum} - ${room.name}`

            entry.onclick = () => {

                EditorManager.openRoom(room)
            }

            container.appendChild(entry)
        })
    },


    // ====================
    // MOBS
    // ====================

    renderMobs() {

        const container =
            document.getElementById('mobs')

        container.innerHTML = ''

        AppState.mobs.forEach(mob => {

            const entry =
                document.createElement('div')

            entry.className =
                'entry'

            entry.innerText =
                `${mob.vnum} - ${mob.name}`

            entry.onclick = () => {

                EditorManager.openMob(mob)
            }

            container.appendChild(entry)
        })
    }
}


// ========================================
// MODAL MANAGER
// ========================================

const ModalManager = {

    open(title) {

        document.getElementById(
            'modalOverlay'
        ).style.display = 'flex'

        document.getElementById(
            'modalTitle'
        ).innerText = title
    },


    close() {

        document.getElementById(
            'modalOverlay'
        ).style.display = 'none'

        document.getElementById(
            'roomEditor'
        ).style.display = 'none'

        document.getElementById(
            'mobEditor'
        ).style.display = 'none'
    }
}


// ========================================
// EDITOR MANAGER
// ========================================

const EditorManager = {

    // ====================
    // OPEN ROOM
    // ====================

    openRoom(room) {

        AppState.selectedRoom = room

        AppState.currentEditor = 'room'

        ModalManager.open(
            `Room Editor - ${room.name}`
        )

        document.getElementById(
            'roomEditor'
        ).style.display = 'flex'

        document.getElementById(
            'mobEditor'
        ).style.display = 'none'

        document.getElementById(
            'room_vnum'
        ).value =
            room.vnum || ''

        document.getElementById(
            'room_name'
        ).value =
            room.name || ''

        document.getElementById(
            'room_description'
        ).value =
            room.description || ''

        document.getElementById(
            'room_region'
        ).value =
            room.region_id || ''

        document.getElementById(
            'room_x'
        ).value =
            room.x || 0

        document.getElementById(
            'room_y'
        ).value =
            room.y || 0

        MapRenderer.render()
    },


    // ====================
    // OPEN MOB
    // ====================

    openMob(mob) {

        AppState.selectedMob = mob

        AppState.currentEditor = 'mob'

        ModalManager.open(
            `Mob Editor - ${mob.name}`
        )

        document.getElementById(
            'mobEditor'
        ).style.display = 'flex'

        document.getElementById(
            'roomEditor'
        ).style.display = 'none'

        document.getElementById(
            'mob_vnum'
        ).value =
            mob.vnum || ''

        document.getElementById(
            'mob_name'
        ).value =
            mob.name || ''

        document.getElementById(
            'mob_description'
        ).value =
            mob.description || ''

        document.getElementById(
            'mob_hp'
        ).value =
            mob.hp || 1

        document.getElementById(
            'mob_damage'
        ).value =
            mob.damage || 1

        document.getElementById(
            'mob_defense'
        ).value =
            mob.defense || 0

        document.getElementById(
            'mob_xp'
        ).value =
            mob.xp || 0

        document.getElementById(
            'mob_gold_min'
        ).value =
            mob.gold_min || 0

        document.getElementById(
            'mob_gold_max'
        ).value =
            mob.gold_max || 0
    }
}


// ========================================
// MAP RENDERER
// ========================================

const MapRenderer = {

    render() {

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        )

        this.drawGrid()

        this.drawRooms()
    },


    // ====================
    // GRID
    // ====================

    drawGrid() {

        if (!AppState.gridEnabled)
            return

        const size = 50

        ctx.strokeStyle =
            '#1f1f1f'

        for (
            let x = 0;
            x < canvas.width;
            x += size
        ) {

            ctx.beginPath()

            ctx.moveTo(x, 0)

            ctx.lineTo(x, canvas.height)

            ctx.stroke()
        }

        for (
            let y = 0;
            y < canvas.height;
            y += size
        ) {

            ctx.beginPath()

            ctx.moveTo(0, y)

            ctx.lineTo(canvas.width, y)

            ctx.stroke()
        }
    },


    // ====================
    // ROOMS
    // ====================

    drawRooms() {

        AppState.rooms.forEach(room => {

            const x =
                room.x || 100

            const y =
                room.y || 100

            // SELECTED
            if (
                AppState.selectedRoom === room
            ) {

                ctx.fillStyle =
                    '#ffcc00'

            } else {

                ctx.fillStyle =
                    '#00ff88'
            }

            ctx.fillRect(
                x,
                y,
                26,
                26
            )

            ctx.fillStyle =
                'white'

            ctx.font =
                '12px Arial'

            ctx.fillText(
                room.vnum,
                x,
                y - 8
            )
        })
    }
}


// ========================================
// UI FUNCTIONS
// ========================================

function closeModal() {

    ModalManager.close()
}


function showTab(tabId) {

    document
        .querySelectorAll('.tabContent')
        .forEach(tab => {

            tab.style.display = 'none'

            tab.classList.remove('active')
        })

    document
        .querySelectorAll('.tabButton')
        .forEach(btn => {

            btn.classList.remove('active')
        })

    const tab =
        document.getElementById(tabId)

    if (tab) {

        tab.style.display = 'block'

        tab.classList.add('active')
    }
}


// ========================================
// SAVE ROOM
// ========================================

function saveRoomForm() {

    if (!AppState.selectedRoom)
        return

    AppState.selectedRoom.vnum =
        parseInt(
            document.getElementById(
                'room_vnum'
            ).value
        )

    AppState.selectedRoom.name =
        document.getElementById(
            'room_name'
        ).value

    AppState.selectedRoom.description =
        document.getElementById(
            'room_description'
        ).value

    AppState.selectedRoom.region_id =
        document.getElementById(
            'room_region'
        ).value

    AppState.selectedRoom.x =
        parseInt(
            document.getElementById(
                'room_x'
            ).value
        )

    AppState.selectedRoom.y =
        parseInt(
            document.getElementById(
                'room_y'
            ).value
        )

    DataManager.saveRoom(
        AppState.selectedRoom
    )

    closeModal()
}


// ========================================
// SAVE MOB
// ========================================

function saveMobForm() {

    if (!AppState.selectedMob)
        return

    AppState.selectedMob.vnum =
        parseInt(
            document.getElementById(
                'mob_vnum'
            ).value
        )

    AppState.selectedMob.name =
        document.getElementById(
            'mob_name'
        ).value

    AppState.selectedMob.description =
        document.getElementById(
            'mob_description'
        ).value

    AppState.selectedMob.hp =
        parseInt(
            document.getElementById(
                'mob_hp'
            ).value
        )

    AppState.selectedMob.damage =
        parseInt(
            document.getElementById(
                'mob_damage'
            ).value
        )

    AppState.selectedMob.defense =
        parseInt(
            document.getElementById(
                'mob_defense'
            ).value
        )

    AppState.selectedMob.xp =
        parseInt(
            document.getElementById(
                'mob_xp'
            ).value
        )

    AppState.selectedMob.gold_min =
        parseInt(
            document.getElementById(
                'mob_gold_min'
            ).value
        )

    AppState.selectedMob.gold_max =
        parseInt(
            document.getElementById(
                'mob_gold_max'
            ).value
        )

    DataManager.saveMob(
        AppState.selectedMob
    )

    closeModal()
}


// ========================================
// NEW ROOM
// ========================================

function newRoom() {

    EditorManager.openRoom({

        vnum: 9999,

        name: 'Nuova Room',

        description: '',

        region_id: 'starting_region',

        x: 100,

        y: 100,

        exits: {}
    })
}


// ========================================
// NEW MOB
// ========================================

function newMob() {

    EditorManager.openMob({

        vnum: 9999,

        name: 'nuovo_mob',

        description: '',

        hp: 10,

        damage: 1,

        defense: 0,

        xp: 10,

        gold_min: 1,

        gold_max: 5
    })
}


// ========================================
// PLACEHOLDERS
// ========================================

function newItem() {

    alert(
        'Item editor in arrivo'
    )
}


function newRegion() {

    alert(
        'Region editor in arrivo'
    )
}


// ========================================
// CANVAS EVENTS
// ========================================

canvas.addEventListener(
    'click',
    function (event) {

        const rect =
            canvas.getBoundingClientRect()

        const mx =
            event.clientX - rect.left

        const my =
            event.clientY - rect.top

        AppState.rooms.forEach(room => {

            const x =
                room.x || 100

            const y =
                room.y || 100

            if (
                mx >= x &&
                mx <= x + 26 &&
                my >= y &&
                my <= y + 26
            ) {

                EditorManager.openRoom(room)
            }
        })
    }
)


// ========================================
// MODAL EVENTS
// ========================================

document.addEventListener(
    'keydown',
    function (event) {

        if (event.key === 'Escape') {

            closeModal()
        }
    }
)


document.getElementById(
    'modalOverlay'
).addEventListener(
    'click',
    function (event) {

        if (
            event.target.id === 'modalOverlay'
        ) {

            closeModal()
        }
    }
)


// ========================================
// RESIZE
// ========================================

function resizeCanvas() {

    canvas.width =
        canvas.clientWidth

    canvas.height =
        canvas.clientHeight

    MapRenderer.render()
}


window.addEventListener(
    'resize',
    resizeCanvas
)


// ========================================
// STARTUP
// ========================================

resizeCanvas()

DataManager.loadRooms()

DataManager.loadMobs()