from flask import Flask, jsonify
from flask_socketio import SocketIO

N = 100

app = Flask(__name__)
socket = SocketIO(app)
room_list = [False] * N
free_room = 0

@app.route("/api/room", methods=["POST"])
def createRoom():
    global free_room
    if not room_list[free_room]:
        room_list[free_room] = True
        room_id = free_room
        free_room += 1
        return jsonify({"Error": "False", "Room ID": room_id})
    else:
        for i in range(free_room, free_room + N):
            if not room_list[i % N]:
                room_list[i % N] = True
                room_id = i
                free_room = i + 1
                return jsonify({"Error": "False", "Room ID": room_id})
        return jsonify({"Error": "True", "Msg": "No Free Room"})

@app.route("/api/room/<rid>", methods=["GET"])
def joinRoom(rid: str):
    if not rid.isdigit():
        return jsonify({"Error": "True", "Msg": "No Valid Room ID"})
    if room_list[int(rid)]:
        return jsonify({"Error": "False"})
    else:
        return jsonify({"Error": "True", "Msg": "Room ID not initialize"})

@app.route("/")
def index():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)
