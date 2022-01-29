from flask import request
from flask_socketio import join_room, leave_room

class SocketRoom:
    __socketRoomID: str
    __socketRoomPeople = {}

    def __init__(self, room_id) -> None:
        self.__socketRoomID = room_id
    
    def getSocketRoomID(self):
        return self.__socketRoomID
    
    def getSocketRoomPeople(self):
        return self.__socketRoomPeople

    def getPax(self):
        return len(self.__socketRoomPeople)

    def isFull(self):
        return len(self.__socketRoomPeople) == 10

    def setSocketRoomID(self, room_id):
        self.getSocketRoomID = room_id
    
    def join(self):
        self.__socketRoomPeople[request.sid] = True
        join_room(self.__socketRoomID)
    
    def leave(self, sid):
        del self.__socketRoomPeople[sid]
        leave_room(self.__socketRoomID)
