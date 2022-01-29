import requests

requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
requests.post("http://127.0.0.1:5000/api/room")
request = requests.get("http://127.0.0.1:5000/api/room/1")
print(request.status_code, request.json())
