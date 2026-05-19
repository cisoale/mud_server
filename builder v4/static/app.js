// ========================================
// REALM BUILDER
// COMPLETE PROFESSIONAL APP.JS
// ========================================


// ========================================
// STATE
// ========================================

const AppState = {

    rooms: [],
    mobs: [],
    regions: [],

    selectedRoom: null,
    selectedMob: null,

    offsetX: 0,
    offsetY: 0,

    gridEnabled: true,

    linkMode: false,
    linkStartRoom: null,
    autoReverse: true
}


// ========================================
// CANVAS
// ========================================

const canvas =
    document.getElementById('mapCanvas')

const ctx =
    canvas.getContext('2d')


// ========================================
// REGION COLORS
// ========================================

const REGION_COLORS = {

    starting_region: '#3fb950',
    forest: '#2e8b57',
    dark_forest: '#5a2a82',
    dungeon: '#8b2f2f',
    village: '#c2a878',
    cave: '#666666',
    swamp: '#556b2f',
    desert: '#d2b55b',
    snow: '#8ecae6',
    unknown: '#777777'
}


// ========================================
// EXIT DIRS
// ========================================

const EXIT_DIRS = [
    'north',
    'south',
    'east',
    'west',
    'up',
    'down'
]


// ========================================
// DATA MANAGER
// ========================================

const DataManager = {

    async loadRooms() {

        const response =
            await fetch('/api/rooms')

        const data =
            await response.json()

        AppState.rooms =
            Array.isArray(data)
                ? data
                : Object.values(data)

        AppState.rooms.forEach((room, index) => {

            if (
                room.pos &&
                typeof room.pos.x === 'number' &&
                typeof room.pos.y === 'number' &&
                (
                    room.pos.x !== 0 ||
                    room.pos.y !== 0
                )
            ) {

                room.x = room.pos.x
                room.y = room.pos.y

            } else {

                room.x =
                    120 + (index % 6) * 140

                room.y =
                    120 + Math.floor(index / 6) * 140
            }
        })

        SidebarManager.renderRooms()
        SidebarManager.renderRegions()

        MapRenderer.render()

    },


    async loadMobs() {

        const response =
            await fetch('/api/mobs')

        const data =
            await response.json()

        AppState.mobs =
            Array.isArray(data)
                ? data
                : Object.values(data)

        SidebarManager.renderMobs()
    },


    async saveRoom(room) {

        room.pos = {

            x: room.x,
            y: room.y
        }

        await fetch('/api/room', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(room)
        })
    },


    async saveMob(mob) {

        await fetch('/api/mob', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(mob)
        })
    }
}


// ========================================
// SIDEBAR MANAGER
// ========================================

const SidebarManager = {

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

            entry.onclick = () =>
                EditorManager.openRoom(room)

            container.appendChild(entry)
        })
    },


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

            entry.onclick = () =>
                EditorManager.openMob(mob)

            container.appendChild(entry)
        })
    },


    renderRegions() {

        const container =
            document.getElementById('regions')

        container.innerHTML = ''

        const map = {}

        AppState.rooms.forEach(room => {

            let region =
                room.region || 'unknown'

            region =
                String(region).trim()

            map[region] = true
        })

        Object.keys(map)
            .sort()
            .forEach(region => {

                const entry =
                    document.createElement('div')

                entry.className =
                    'regionEntry'

                const color =
                    document.createElement('div')

                color.className =
                    'regionColor'

                color.style.background =
                    REGION_COLORS[region] || '#00ff88'

                const label =
                    document.createElement('div')

                label.innerText =
                    region

                entry.appendChild(color)
                entry.appendChild(label)

                container.appendChild(entry)
            })
    }
}

// ========================================
// HELP MODAL
// ========================================

function openHelpModal() {

    document.getElementById(
        'helpOverlay'
    ).style.display = 'flex'
}


function closeHelpModal() {

    document.getElementById(
        'helpOverlay'
    ).style.display = 'none'
}

// ========================================
// VALIDATION
// ========================================

let validationErrors = []


function validateWorld() {

    validationErrors = []

    const roomMap = {}



    // ====================================
    // BUILD MAP
    // ====================================

    AppState.rooms.forEach(room => {

        if (roomMap[room.vnum]) {

            validationErrors.push({

                vnum: room.vnum,

                message:
                    `Duplicate room vnum: ${room.vnum}`
            })
        }

        roomMap[room.vnum] = room
    })



    // ====================================
    // EXIT CHECKS
    // ====================================

    AppState.rooms.forEach(room => {

        if (!room.exits)
            return

        Object.entries(room.exits)
            .forEach(([dir, exit]) => {

                if (!roomMap[exit.to]) {

                    validationErrors.push({

                        vnum: room.vnum,

                        message:
                            `Room ${room.vnum} ${dir} -> ${exit.to} missing`
                    })

                    return
                }


                // ============================
                // REVERSE CHECK
                // ============================

                const reverse =
                    reverseDirection(dir)

                const target =
                    roomMap[exit.to]

                if (
                    target.exits &&
                    target.exits[reverse]
                ) {

                    if (
                        target.exits[reverse].to != room.vnum
                    ) {

                        validationErrors.push({

                            vnum: room.vnum,

                            message:
                                `Missing reverse exit ${room.vnum} ${dir}`
                        })
                    }

                } else {

                    validationErrors.push({

                        vnum: room.vnum,

                        message:
                            `Missing reverse exit ${room.vnum} ${dir}`
                    })
                }
            })
    })



    // ====================================
    // UPDATE BUTTON
    // ====================================

    const button =
        document.getElementById(
            'validationButton'
        )

    if (validationErrors.length > 0) {

        button.classList.add(
            'hasErrors'
        )

    } else {

        button.classList.remove(
            'hasErrors'
        )
    }
}


function openValidationModal() {

    validateWorld()

    const content =
        document.getElementById(
            'validationContent'
        )

    content.innerHTML = ''


    // ====================================
    // NO ERRORS
    // ====================================

    if (validationErrors.length === 0) {

        content.innerHTML = `
            <div class="validationSuccess">
                No validation errors found.
            </div>
        `

    } else {

        validationErrors.forEach(errorData => {

            const div =
                document.createElement('div')

            div.className =
                'validationError'

            div.innerText =
                errorData.message


            // ====================================
            // CLICK ROOM
            // ====================================

            if (errorData.vnum !== undefined) {

                div.onclick = () => {

                    focusRoom(
                        errorData.vnum
                    )
                }
            }

            content.appendChild(div)
        })
    }

    document.getElementById(
        'validationOverlay'
    ).style.display = 'flex'
}


function closeValidationModal() {

    document.getElementById(
        'validationOverlay'
    ).style.display = 'none'
}


// ========================================
// FOCUS ROOM
// ========================================

function focusRoom(vnum) {

    const room =
        AppState.rooms.find(r =>
            r.vnum == vnum
        )

    if (!room)
        return


    // ====================================
    // CENTER CAMERA
    // ====================================

    AppState.offsetX =
        canvas.width / 2 - room.x - 13

    AppState.offsetY =
        canvas.height / 2 - room.y - 13


    // ====================================
    // SELECT ROOM
    // ====================================

    AppState.selectedRoom = room

    MapRenderer.render()


    // ====================================
    // OPEN ROOM EDITOR
    // ====================================

    closeValidationModal()

    EditorManager.openRoom(room)
}
// ========================================
// MODALS
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
// EDITORS
// ========================================

const EditorManager = {

    openRoom(room) {

        AppState.selectedRoom = room

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
            room.region || ''

        document.getElementById(
            'room_x'
        ).value =
            room.x || 0

        document.getElementById(
            'room_y'
        ).value =
            room.y || 0

        loadAllExits(room)

        MapRenderer.render()
    },


    openMob(mob) {

        AppState.selectedMob = mob

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
    }
}


// ========================================
// EXIT SYSTEM
// ========================================

function loadAllExits(room) {

    const exits =
        room.exits || {}

    EXIT_DIRS.forEach(dir => {

        const exit =
            exits[dir] || {}

        const to =
            document.getElementById(
                `exit_${dir}_to`
            )

        if (to)
            to.value = exit.to || ''

                ;[
                    'door',
                    'closed',
                    'locked',
                    'secret',
                    'blocked'
                ].forEach(flag => {

                    const el =
                        document.getElementById(
                            `exit_${dir}_${flag}`
                        )

                    if (el)
                        el.checked =
                            exit[flag] || false
                })

        const key =
            document.getElementById(
                `exit_${dir}_key`
            )

        if (key)
            key.value =
                exit.key || ''
    })
}


function buildExit(dir) {

    const to =
        document.getElementById(
            `exit_${dir}_to`
        )?.value

    if (!to)
        return null

    return {

        to: parseInt(to),

        door:
            document.getElementById(
                `exit_${dir}_door`
            )?.checked || false,

        closed:
            document.getElementById(
                `exit_${dir}_closed`
            )?.checked || false,

        locked:
            document.getElementById(
                `exit_${dir}_locked`
            )?.checked || false,

        secret:
            document.getElementById(
                `exit_${dir}_secret`
            )?.checked || false,

        blocked:
            document.getElementById(
                `exit_${dir}_blocked`
            )?.checked || false,

        key:
            document.getElementById(
                `exit_${dir}_key`
            )?.value || ''
    }
}


// ========================================
// LINE HIT TEST
// ========================================

function pointNearLine(
    px,
    py,
    x1,
    y1,
    x2,
    y2
) {

    const A = px - x1
    const B = py - y1

    const C = x2 - x1
    const D = y2 - y1

    const dot =
        A * C + B * D

    const lenSq =
        C * C + D * D

    let param = -1

    if (lenSq !== 0) {

        param = dot / lenSq
    }

    let xx
    let yy

    if (param < 0) {

        xx = x1
        yy = y1

    } else if (param > 1) {

        xx = x2
        yy = y2

    } else {

        xx = x1 + param * C
        yy = y1 + param * D
    }

    const dx = px - xx
    const dy = py - yy

    return Math.sqrt(
        dx * dx +
        dy * dy
    ) < 8
}


// ========================================
// DELETE EXIT TOOL
// ========================================

async function tryDeleteExit(
    mx,
    my
) {

    for (const room of AppState.rooms) {

        if (!room.exits)
            continue

        for (const [dir, exit] of Object.entries(room.exits)) {

            if (!exit.to)
                continue

            const target =
                AppState.rooms.find(r =>
                    r.vnum == exit.to
                )

            if (!target)
                continue

            const x1 =
                room.x + 13

            const y1 =
                room.y + 13

            const x2 =
                target.x + 13

            const y2 =
                target.y + 13

            if (
                pointNearLine(
                    mx,
                    my,
                    x1,
                    y1,
                    x2,
                    y2
                )
            ) {

                const confirmDelete =
                    confirm(
                        `Delete exit ${dir}?`
                    )

                if (!confirmDelete)
                    return true


                delete room.exits[dir]

                await DataManager.saveRoom(
                    room
                )


                const reverse =
                    reverseDirection(dir)

                if (
                    target.exits &&
                    target.exits[reverse] &&
                    target.exits[reverse].to == room.vnum
                ) {

                    const removeReverse =
                        confirm(
                            'Delete reverse exit too?'
                        )

                    if (removeReverse) {

                        delete target.exits[reverse]

                        await DataManager.saveRoom(
                            target
                        )
                    }
                }

                MapRenderer.render()

                return true
            }
        }
    }

    return false
}


// ========================================
// LINK MODE
// ========================================

function toggleLinkMode() {

    AppState.linkMode =
        !AppState.linkMode

    AppState.linkStartRoom =
        null

    if (AppState.linkMode) {

        alert(
            'Link Mode Attivato'
        )

    } else {

        alert(
            'Link Mode Disattivato'
        )
    }
}


function getDirection(from, to) {

    const dx =
        to.x - from.x

    const dy =
        to.y - from.y

    if (
        Math.abs(dx) >
        Math.abs(dy)
    ) {

        if (dx > 0)
            return 'east'

        return 'west'
    }

    if (dy > 0)
        return 'south'

    return 'north'
}


function reverseDirection(dir) {

    const map = {

        north: 'south',
        south: 'north',
        east: 'west',
        west: 'east',
        up: 'down',
        down: 'up'
    }

    return map[dir]
}


async function createLink(
    fromRoom,
    toRoom
) {

    const dir =
        getDirection(
            fromRoom,
            toRoom
        )

    if (!fromRoom.exits)
        fromRoom.exits = {}

    fromRoom.exits[dir] = {

        to: toRoom.vnum
    }


    if (AppState.autoReverse) {

        const reverse =
            reverseDirection(dir)

        if (!toRoom.exits)
            toRoom.exits = {}

        toRoom.exits[reverse] = {

            to: fromRoom.vnum
        }

        await DataManager.saveRoom(
            toRoom
        )
    }

    await DataManager.saveRoom(
        fromRoom
    )

    MapRenderer.render()

    validateWorld()
}


// ========================================
// MAP RENDERER
// ========================================

const MapRenderer = {

    render() {

        ctx.setTransform(
            1,
            0,
            0,
            1,
            0,
            0
        )

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        )

        ctx.translate(
            AppState.offsetX,
            AppState.offsetY
        )

        this.drawGrid()
        this.drawExits()
        this.drawRooms()
    },


    drawGrid() {

        if (!AppState.gridEnabled)
            return

        ctx.strokeStyle =
            '#1f1f1f'

        for (
            let x = -5000;
            x < 5000;
            x += 50
        ) {

            ctx.beginPath()

            ctx.moveTo(x, -5000)

            ctx.lineTo(x, 5000)

            ctx.stroke()
        }

        for (
            let y = -5000;
            y < 5000;
            y += 50
        ) {

            ctx.beginPath()

            ctx.moveTo(-5000, y)

            ctx.lineTo(5000, y)

            ctx.stroke()
        }
    },


    drawExits() {

        ctx.lineWidth = 3

        AppState.rooms.forEach(room => {

            if (!room.exits)
                return

            const startX =
                room.x + 13

            const startY =
                room.y + 13

            Object.entries(room.exits)
                .forEach(([dir, exit]) => {

                    if (!exit.to)
                        return

                    const target =
                        AppState.rooms.find(r =>
                            r.vnum == exit.to
                        )

                    if (!target)
                        return

                    const endX =
                        target.x + 13

                    const endY =
                        target.y + 13

                    if (exit.secret) {

                        ctx.strokeStyle =
                            '#888'

                        ctx.setLineDash([6, 6])

                    } else if (exit.locked) {

                        ctx.strokeStyle =
                            '#ff4444'

                        ctx.setLineDash([])

                    } else {

                        ctx.strokeStyle =
                            '#666'

                        ctx.setLineDash([])
                    }

                    ctx.beginPath()

                    ctx.moveTo(
                        startX,
                        startY
                    )

                    ctx.lineTo(
                        endX,
                        endY
                    )

                    ctx.stroke()
                })
        })

        ctx.setLineDash([])
    },


    drawRooms() {

        AppState.rooms.forEach(room => {

            const x = room.x
            const y = room.y

            const color =
                REGION_COLORS[
                room.region || 'unknown'
                ] || '#00ff88'

            if (
                AppState.linkStartRoom === room
            ) {

                ctx.fillStyle =
                    '#00d0ff'

            } else if (
                AppState.selectedRoom === room
            ) {

                ctx.fillStyle =
                    '#ffd000'

            } else {

                ctx.fillStyle =
                    color
            }

            ctx.fillRect(
                x,
                y,
                26,
                26
            )

            ctx.strokeStyle =
                '#000'

            ctx.strokeRect(
                x,
                y,
                26,
                26
            )

            ctx.fillStyle =
                '#fff'

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
// CAMERA + ROOM DRAG
// ========================================

let isDraggingMap = false

let draggedRoom = null

let dragStartX = 0
let dragStartY = 0

let mouseMoved = false


canvas.addEventListener(
    'mousedown',
    function (event) {

        if (AppState.linkMode)
            return

        mouseMoved = false

        const rect =
            canvas.getBoundingClientRect()

        const mx =
            event.clientX -
            rect.left -
            AppState.offsetX

        const my =
            event.clientY -
            rect.top -
            AppState.offsetY

        draggedRoom = null

        for (const room of AppState.rooms) {

            if (
                mx >= room.x &&
                mx <= room.x + 26 &&
                my >= room.y &&
                my <= room.y + 26
            ) {

                draggedRoom = room

                break
            }
        }

        dragStartX =
            event.clientX

        dragStartY =
            event.clientY

        if (!draggedRoom) {

            isDraggingMap = true
        }
    }
)


window.addEventListener(
    'mouseup',
    async function () {

        isDraggingMap = false

        if (draggedRoom && mouseMoved) {

            await DataManager.saveRoom(
                draggedRoom
            )
        }

        draggedRoom = null
    }
)


window.addEventListener(
    'mousemove',
    function (event) {

        if (AppState.linkMode)
            return

        const dx =
            event.clientX - dragStartX

        const dy =
            event.clientY - dragStartY

        if (
            Math.abs(dx) > 2 ||
            Math.abs(dy) > 2
        ) {

            mouseMoved = true
        }

        dragStartX =
            event.clientX

        dragStartY =
            event.clientY

        if (draggedRoom && mouseMoved) {

            draggedRoom.x += dx
            draggedRoom.y += dy

            MapRenderer.render()

            return
        }

        if (isDraggingMap && mouseMoved) {

            AppState.offsetX += dx
            AppState.offsetY += dy

            MapRenderer.render()
        }
    }
)


// ========================================
// ROOM CLICK
// ========================================

canvas.addEventListener(
    'click',
    function (event) {

        if (
            mouseMoved &&
            !AppState.linkMode
        )
            return

        const rect =
            canvas.getBoundingClientRect()

        const mx =
            event.clientX -
            rect.left -
            AppState.offsetX

        const my =
            event.clientY -
            rect.top -
            AppState.offsetY


        // ====================================
        // ALT CLICK DELETE EXIT
        // ====================================

        if (event.altKey) {

            tryDeleteExit(
                mx,
                my
            )

            return
        }


        for (const room of AppState.rooms) {

            if (
                mx >= room.x &&
                mx <= room.x + 26 &&
                my >= room.y &&
                my <= room.y + 26
            ) {

                // LINK MODE

                if (AppState.linkMode) {

                    if (!AppState.linkStartRoom) {

                        AppState.linkStartRoom =
                            room

                        MapRenderer.render()

                        return
                    }

                    if (
                        AppState.linkStartRoom !== room
                    ) {

                        createLink(
                            AppState.linkStartRoom,
                            room
                        )
                    }

                    AppState.linkStartRoom =
                        null

                    MapRenderer.render()

                    return
                }


                // NORMAL MODE

                EditorManager.openRoom(room)

                return
            }
        }
    }
)


// ========================================
// SAVE
// ========================================

function saveRoomForm() {

    const room =
        AppState.selectedRoom

    room.vnum =
        parseInt(
            document.getElementById(
                'room_vnum'
            ).value
        )

    room.name =
        document.getElementById(
            'room_name'
        ).value

    room.description =
        document.getElementById(
            'room_description'
        ).value

    room.region =
        document.getElementById(
            'room_region'
        ).value

    room.x =
        parseInt(
            document.getElementById(
                'room_x'
            ).value
        )

    room.y =
        parseInt(
            document.getElementById(
                'room_y'
            ).value
        )

    room.exits = {}

    EXIT_DIRS.forEach(dir => {

        const exit =
            buildExit(dir)

        if (exit)
            room.exits[dir] = exit
    })

    DataManager.saveRoom(room)

    closeModal()

    MapRenderer.render()

    validateWorld()
}


function saveMobForm() {

    const mob =
        AppState.selectedMob

    mob.vnum =
        parseInt(
            document.getElementById(
                'mob_vnum'
            ).value
        )

    mob.name =
        document.getElementById(
            'mob_name'
        ).value

    mob.description =
        document.getElementById(
            'mob_description'
        ).value

    mob.hp =
        parseInt(
            document.getElementById(
                'mob_hp'
            ).value
        )

    mob.damage =
        parseInt(
            document.getElementById(
                'mob_damage'
            ).value
        )

    mob.defense =
        parseInt(
            document.getElementById(
                'mob_defense'
            ).value
        )

    DataManager.saveMob(mob)

    closeModal()
}

// ========================================
// DELETE ROOM
// ========================================

async function deleteCurrentRoom() {

    const room =
        AppState.selectedRoom

    if (!room)
        return


    // ====================================
    // CONFIRM
    // ====================================

    const confirmed =
        confirm(
            `Delete room ${room.vnum}?`
        )

    if (!confirmed)
        return


    // ====================================
    // REMOVE LINKS TO ROOM
    // ====================================

    AppState.rooms.forEach(otherRoom => {

        if (!otherRoom.exits)
            return

        Object.entries(otherRoom.exits)
            .forEach(([dir, exit]) => {

                if (
                    exit.to == room.vnum
                ) {

                    delete otherRoom.exits[dir]

                    DataManager.saveRoom(
                        otherRoom
                    )
                }
            })
    })


    // ====================================
    // REMOVE ROOM
    // ====================================

    AppState.rooms =
        AppState.rooms.filter(r =>
            r !== room
        )


    // ====================================
    // SAVE DELETE
    // ====================================

    await fetch('/api/delete_room', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({

            vnum: room.vnum
        })
    })


    // ====================================
    // CLEAN STATE
    // ====================================

    AppState.selectedRoom =
        null


    // ====================================
    // UI UPDATE
    // ====================================

    closeModal()

    SidebarManager.renderRooms()

    validateWorld()

    MapRenderer.render()
}
// ========================================
// NEW
// ========================================

function newRoom() {

    EditorManager.openRoom({

        vnum: 9999,
        name: 'Nuova Room',
        description: '',
        region: 'starting_region',
        x: 100,
        y: 100,
        exits: {}
    })
}


function newMob() {

    EditorManager.openMob({

        vnum: 9999,
        name: 'Nuovo Mob',
        description: '',
        hp: 10,
        damage: 1,
        defense: 0
    })
}


function newRegion() {

    const name =
        prompt('Nome nuova regione:')

    if (!name)
        return

    SidebarManager.renderRegions()
}


// ========================================
// MODALS
// ========================================

function closeModal() {

    ModalManager.close()
}


document.addEventListener(
    'keydown',
    function (event) {

        if (event.key === 'Escape')
            closeModal()
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


// ========================================
// INITIAL VALIDATION
// ========================================

setTimeout(
    validateWorld,
    500
)