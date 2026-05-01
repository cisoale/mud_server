import os
from config import ITEMS_DIR
# ✅ GIUSTO
from normalizers import normalize_item
from services.file_service import load_all_json, save_json, delete_file

def get_items():
    return load_all_json(ITEMS_DIR)

def save_item(data):
    item = normalize_item(data)
    path = os.path.join(ITEMS_DIR, f"{item['name']}.json")
    save_json(path, item)
    return item

def delete_item(name):
    path = os.path.join(ITEMS_DIR, f"{name}.json")
    return delete_file(path)