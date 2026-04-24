from flask import Flask, request
import os, json

from flask import send_from_directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ITEMS = os.path.abspath(os.path.join(BASE_DIR, "../data/items"))
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "item_editor.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(BASE_DIR, path)
app = Flask(__name__)




@app.route("/items")
def get_items():
    res = []
    for f in os.listdir(ITEMS):
        if f.endswith(".json"):
            with open(os.path.join(ITEMS, f), encoding="utf-8") as fp:
                res.append(json.load(fp))
    return res


@app.route("/save_item", methods=["POST"])
def save_item():
    data = request.json

    path = os.path.join(ITEMS, f"{data['name']}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return {"status": "ok"}

####
@app.route("/delete_item", methods=["POST"])
def delete_item():

    data = request.json
    name = data.get("name")

    if not name:
        return {"status": "error"}

    path = os.path.join(ITEMS, f"{name}.json")

    if not os.path.exists(path):
        return {"status": "error"}

    os.remove(path)

    print("[DELETE ITEM]", name)

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(port=5002, debug=True)