import socketio
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

sio = socketio.Client(logger=True)

@sio.event
def connect():
    print('connection established')
    sio.emit("join", {"Room ID": room_id})

@sio.on("Server response")
def server_response(data):
    print(data)

sio.connect('http://127.0.0.1:5000', namespaces="/websocket", transports=['websocket'])
sio.wait()
