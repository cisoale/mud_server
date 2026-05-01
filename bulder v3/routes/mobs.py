from flask import Blueprint, request
from services.mob_service import get_mobs, save_mob, delete_mob

mobs_bp = Blueprint("mobs", __name__)

@mobs_bp.route("/mobs", methods=["GET"])
def mobs_list():
    return {"mobs": get_mobs()}

@mobs_bp.route("/mobs", methods=["POST"])
def mobs_create():
    mob = save_mob(request.json)
    return {"status": "ok", "mob": mob}

@mobs_bp.route("/mobs/<name>", methods=["DELETE"])
def mobs_delete(name):
    if delete_mob(name):
        return {"status": "ok"}
    return {"status": "error"}, 404