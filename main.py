from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, join_room, leave_room, rooms, emit

N = 100

app = Flask(__name__)
socket = SocketIO(app)
room_list = [False] * N
free_room = 0
room_host = {}


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
    return render_template('socket_test.html')


@socket.on("join", namespace="/websocket")
def joinSocketRoom(json_data):
    print(json_data)  # Debug only
    room_id = json_data['Room ID']
    ishost = json_data["Host"]
    if ishost == "True":
        room_host[request.sid] = room_id
    join_room(f"{room_id}A")
    join_room(f"{room_id}B")
    print(rooms(request.sid))  # Debug only
    emit("server_response", {"Error": "False"})


@socket.on("disconnect", namespace="/websocket")
def leaveSocketRoom(json_data = {}):
    if room_id := room_host.get(request.sid):
        for room in rooms(request.sid):
            leave_room(room)
        emit("force_exit", {"Error": "False", "Msg": "Host exit"}, to=f"{room_id}A")
    else:
        for room in rooms(request.sid):
            leave_room(room)
    emit("server_response", {"Error": "False", "Msg": "Bye"})


if __name__ == "__main__":
    socket.run(app, debug=True, host="0.0.0.0")
