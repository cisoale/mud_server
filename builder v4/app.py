import json

from flask import Flask
from flask import request
from flask import jsonify
from flask import send_from_directory

from services.room_service import get_rooms
from services.room_service import save_room

from services.mob_service import get_mobs
from services.mob_service import save_mob


app = Flask(__name__)


@app.route("/")
def index():

    return send_from_directory(
        "static",
        "index.html"
    )


@app.route("/api/rooms")
def api_rooms():

    try:

        rooms = get_rooms()

        safe_rooms = []

        for room in rooms:

            clean = {}

            for key, value in room.items():

                try:

                    json.dumps(value)

                    clean[key] = value

                except:

                    clean[key] = str(value)

            safe_rooms.append(clean)

        return jsonify(safe_rooms)

    except Exception as e:

        print("API ROOMS ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/mobs")
def api_mobs():

    try:

        mobs = get_mobs()

        safe_mobs = []

        for mob in mobs:

            clean = {}

            for key, value in mob.items():

                try:

                    json.dumps(value)

                    clean[key] = value

                except:

                    clean[key] = str(value)

            safe_mobs.append(clean)

        return jsonify(safe_mobs)

    except Exception as e:

        print("API MOBS ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/room", methods=["POST"])
def api_save_room():

    try:

        data = request.json

        save_room(data)

        return jsonify({
            "ok": True
        })

    except Exception as e:

        print("SAVE ROOM ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/mob", methods=["POST"])
def api_save_mob():

    try:

        data = request.json

        save_mob(data)

        return jsonify({
            "ok": True
        })

    except Exception as e:

        print("SAVE MOB ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


@app.route('/<path:path>')
def static_proxy(path):

    return send_from_directory(
        'static',
        path
    )


if __name__ == "__main__":

    print("=== BUILDER AVVIATO ===")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )