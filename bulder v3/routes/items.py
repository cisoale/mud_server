from flask import Blueprint, request
from services.item_service import get_items, save_item, delete_item

items_bp = Blueprint("items", __name__)

@items_bp.route("/items", methods=["GET"])
def items_list():
    return {"items": get_items()}

@items_bp.route("/items", methods=["POST"])
def items_create():
    item = save_item(request.json)
    return {"status": "ok", "item": item}

@items_bp.route("/items/<name>", methods=["DELETE"])
def items_delete(name):
    if delete_item(name):
        return {"status": "ok"}
    return {"status": "error"}, 404