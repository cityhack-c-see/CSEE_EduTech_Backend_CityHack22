import random

from flask import Flask, jsonify
from flask_socketio import SocketIO, rooms

app = Flask(__name__)
socket = SocketIO(app)
room_list = [False] * 100
free_room = 0


@app.route('/api/room', methods=['GET'])
def createRoom():
    global free_room
    if not room_list[free_room]:
        room_id = free_room
        free_room += 1
        return jsonify({'Error': 'False', 'Room ID': room_id})
    else:
        for i in range(free_room, (free_room + 100)):
            if not room_list[i % 100]:
                room_id = i
                free_room = i + 1
                return jsonify({'Error': 'False', 'Room ID': room_id})
        return jsonify({'Error': 'True', 'Msg': 'No Free Room'})


@app.route('/')
def index():
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True)
