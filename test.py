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
