from flask import Flask
from routes.rooms import rooms_bp
from routes.items import items_bp
from routes.mobs import mobs_bp

# =========================
# CONFIG APP
# =========================

app = Flask(__name__, static_folder="ui")

# =========================
# REGISTER API ROUTES
# =========================

app.register_blueprint(rooms_bp)
app.register_blueprint(items_bp)
app.register_blueprint(mobs_bp)

# =========================
# ROUTE FRONTEND
# =========================

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/rooms.html")
def rooms_page():
    return app.send_static_file("rooms.html")

@app.route("/items.html")
def items_page():
    return app.send_static_file("items.html")

@app.route("/mobs.html")
def mobs_page():
    return app.send_static_file("mobs.html")

# =========================
# DEBUG START
# =========================

if __name__ == "__main__":
    print("=== BUILDER V3 (FIXED) ===")
    print("UI → http://127.0.0.1:5005/")
    print("Rooms → http://127.0.0.1:5005/rooms.html")
    print("Items → http://127.0.0.1:5005/items.html")
    print("Mobs → http://127.0.0.1:5005/mobs.html")

    app.run(debug=True, port=5005)