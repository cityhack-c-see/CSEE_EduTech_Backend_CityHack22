import random

from flask import Flask, jsonify
from flask_socketio import SocketIO, rooms

app = Flask(__name__)
socket = SocketIO(app)
room_list = [False] * 10000
free_room = 0


@app.route('/api/room', methods=['GET'])
def createRoom():
    room_id = 1
    return jsonify({'Room ID': room_id})


@app.route('/')
def index():
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True)
