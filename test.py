from socketio import Client
import requests

r = requests.post("http://127.0.0.1:5000/api/room")
room_id = r.json()["Room ID"]
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
request = requests.get(f"http://127.0.0.1:5000/api/room/{room_id}")
print(request.status_code, request.json())

sio = Client(logger=True)


@sio.event
def connect():
    print('connection established')
    sio.emit("join", data={"Room ID": 1})


@sio.event
def server_response(data):
    print(data)


sio.connect('http://14.198.186.160:5000/websocket')
print(sio.connected)
