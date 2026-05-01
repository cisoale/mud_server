import json, os

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_all_json(directory):
    ensure_dir(directory)
    res = []

    for f in os.listdir(directory):
        if f.endswith(".json"):
            path = os.path.join(directory, f)
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
                data["_file"] = f
                res.append(data)

    return res

def save_json(path, data):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
        return True
    return False