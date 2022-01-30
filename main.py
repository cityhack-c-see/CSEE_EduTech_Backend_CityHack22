import json

from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, join_room, leave_room, rooms, emit
from room import Room
from threading import Thread
import time

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
        free_room %= 100
        thread = Thread(target=threaded_task, args=(room_id,))
        thread.daemon = True
        thread.start()
        return jsonify({"Error": "False", "Room ID": room_id})
    else:
        for i in range(free_room, free_room + NUMBER_OF_ROOMS):
            if not room_list[i % NUMBER_OF_ROOMS].isOccupied():
                room_list[free_room].setOccupied(True)
                room_id = i
                free_room = (i + 1) % 100
                thread = Thread(target=threaded_task, args=(room_id,))
                thread.daemon = True
                thread.start()
                return jsonify({"Error": "False", "Room ID": room_id})
        return jsonify({"Error": "True", "Msg": "No Free Room"})


def threaded_task(room_id):
    time.sleep(10)
    if room_list[room_id].getHost() == None:
        room_list[room_id].setOccupied(False)


@app.route("/api/room/<rid>", methods=["GET"])
def joinRoom(rid: str):
    if not rid.isdigit():
        return jsonify({"Error": "True", "Msg": "No Valid Room ID"})
    if int(rid) > NUMBER_OF_ROOMS - 1 or int(rid) < 0:
        return jsonify({"Error": "True", "Msg": "Room ID is not valid"})
    if room_list[int(rid)].isOccupied():
        return jsonify({"Error": "False"})  # Next step Websocket, discuss required
    elif room_list[int(rid)].getStudentCounter() == 100:
        return jsonify({"Error": "True", "Msg": "This room is full"})
    else:
        return jsonify({"Error": "True", "Msg": "Room ID not initialize"})


@socket.on("join", namespace="/websocket")
def joinSocketRoom(json_data):
    room_id = json_data['Room ID']
    if not room_id.isdigit():
        emit("server_response", {"Error": "True", "Msg": "Room ID not valid"})
    room_id = int(room_id)
    if NUMBER_OF_ROOMS - 1 >= room_id >= 0:
        ishost = json_data["Host"]
        bigRoom: Room = room_list[room_id]
        if bigRoom.isOccupied():

            if ishost == "True":

                bigRoom.hostJoin()
                emit("server_response", {"Error": "False", "Msg": "Success"})
            else:
                if groupID := bigRoom.studentJoin():
                    emit("server_response", {"Error": "False", "Msg": groupID})
                else:
                    emit("server_response", {"Error": "True", "Msg": "Room Full"})
        else:
            emit("server_response", {"Error": "True", "Msg": "Room is not available"})
    else:
        emit("server_response", {"Error": "True", "Msg": "Room ID is not valid"})


@socket.on("disconnect", namespace="/websocket")
def leaveSocketRoom(json_data={}):
    if room_id := json_data.get("Room ID"):
        bigRoom = room_list[room_id]
        if groupID := json_data.get("Group ID"):
            bigRoom.studentLeave(groupID)
        else:
            bigRoom.hostLeave()
    else:
        if len(rooms(request.sid)) != 1:
            for i in rooms(request.sid):
                if i != request.sid:
                    if type(i) == int:
                        room_id = i
                    else:
                        groupID = i
            bigRoom = room_list[int(room_id)]
            if request.sid == bigRoom.getHost():
                bigRoom.hostLeave()
            else:
                bigRoom.studentLeave(groupID)
    emit("server_response", {"Error": "False", "Msg": "Bye"})


def getRoomBySID(sid):
    for i in range(NUMBER_OF_ROOMS):
        if room_list[i].getHost() == sid:
            return i
    return -1


@socket.on('client_request', namespace="/websocket")
def drawData(data):
    try:
        json_data = json.loads(data)
    except:
        json_data = data
    room_id = json_data['Room ID']
    if room_id.isdigit():
        emit('server_response', data, room=int(room_id))
    else:
        emit('server_response', data, room=room_id)


if __name__ == "__main__":
    socket.run(app, debug=True, host="0.0.0.0")
