import requests

r = requests.post("http://14.198.186.160:5000/api/room")
room_id = r.json()["Room ID"]
request = requests.get(f"http://14.198.186.160:5000/api/room/{room_id}")
print(request.status_code, request.json())
