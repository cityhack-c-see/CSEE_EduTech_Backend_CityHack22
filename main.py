from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, join_room, leave_room, rooms, emit
from room import Room

MAX_STUDENT_PER_ROOM = 100
NUMBER_OF_ROOMS = 100
MAX_STUDENT_PER_GROUP = 10

app = Flask(__name__)
socket = SocketIO(app)
room_list = [Room(x) for x in range(NUMBER_OF_ROOMS)]
free_room = 0


@app.route("/api/room", methods=["POST"])
def createRoom():
    global free_room
    if not room_list[free_room].isOccupied():
        room_list[free_room].setOccupied(True)
        room_id = free_room
        free_room += 1
        return jsonify({"Error": "False", "Room ID": room_id})
    else:
        for i in range(free_room, free_room + NUMBER_OF_ROOMS):
            if not room_list[i % NUMBER_OF_ROOMS].isOccupied():
                room_list[free_room].setOccupied(True)
                room_id = i
                free_room = i + 1
                return jsonify({"Error": "False", "Room ID": room_id})
        return jsonify({"Error": "True", "Msg": "No Free Room"})


@app.route("/api/room/<rid>", methods=["GET"])
def joinRoom(rid: str):
    if not rid.isdigit():
        return jsonify({"Error": "True", "Msg": "No Valid Room ID"})
    if room_list[int(rid)].isOccupied():
        return jsonify({"Error": "False"})  # Next step Websocket, discuss required
    elif room_list[int(rid)].getStudentCounter() == 100:
        return jsonify({"Error": "True", "Msg": "This room is full"})
    else:
        return jsonify({"Error": "True", "Msg": "Room ID not initialize"})


@app.route("/")
def index():
    return render_template('socket_test.html')  # Debug only


@socket.on("join", namespace="/websocket")
def joinSocketRoom(json_data):
    print(json_data)  # Debug only
    room_id = json_data['Room ID']
    if not room_id.isdigit():
        emit("server_response", {"Error": "True", "Msg": "Room ID not valid"})
    room_id = int(room_id)
    ishost = json_data["Host"]
    room: Room = room_list[room_id]
    if ishost == "True":
        room.hostJoin()
        emit("server_response", {"Error": "False", "Msg": "Success"})
    else:
        if groupID := room.studentJoin():
            emit("server_response", {"Error": "False", "Msg": groupID})
        else:
            emit("server_response", {"Error": "True", "Msg": "Room Full"})
    print(rooms(request.sid))  # Debug only


@socket.on("disconnect", namespace="/websocket")
def leaveSocketRoom(json_data={}):
    if room_id := json_data.get("Room ID"):

        room = room_list[room_id]
        if groupID := json_data.get("Group ID"):
            room.studentLeave(groupID)
        else:
            room.hostLeave()

    else:
        for i in rooms(request.sid):
            if i != request.sid:
                if i.isDigit():
                    room_id = i
                else:
                    groupID = i
        room = room_list[room_id]
        if request.sid == room.getHost():
            room.hostLeave()
        else:
            room.studentLeave(groupID)
    emit("server_response", {"Error": "False", "Msg": "Bye"})


def getRoomBySID(sid):
    for i in range(NUMBER_OF_ROOMS):
        if room_list[i].getHost() == sid:
            return i
    return -1


if __name__ == "__main__":
    socket.run(app, debug=True, host="0.0.0.0")
