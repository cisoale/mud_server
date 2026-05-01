import os
from config import MOBS_DIR
from normalizers import normalize_mob
from services.file_service import load_all_json, save_json, delete_file

def get_mobs():
    return load_all_json(MOBS_DIR)

def save_mob(data):
    mob = normalize_mob(data)
    path = os.path.join(MOBS_DIR, f"{mob['name']}.json")
    save_json(path, mob)
    return mob

def delete_mob(name):
    path = os.path.join(MOBS_DIR, f"{name}.json")
    return delete_file(path)