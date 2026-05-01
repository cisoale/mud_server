from flask import Blueprint, request
from services.room_service import get_rooms, save_room, delete_room

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("/rooms", methods=["GET"])
def rooms_list():
    return {"rooms": get_rooms()}

@rooms_bp.route("/rooms", methods=["POST"])
def rooms_save():
    room = request.json
    save_room(room)
    return {"status": "ok"}

@rooms_bp.route("/rooms/<int:vnum>", methods=["DELETE"])
def rooms_delete(vnum):
    if delete_room(vnum):
        return {"status": "ok"}
    return {"status": "error"}, 404