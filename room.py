from socketroom import SocketRoom
from flask import request
from flask_socketio import join_room, leave_room

class Room:
    __roomID: str
    __host = None
    __Occupied = False
    __studentCounter = 0
    __socketRoomList = [SocketRoom(f"{__roomID}A")]

    def __init__(self, roomID):
        self.__roomID = roomID

    def getRoomID(self):
        return self.__roomID

    def getHost(self):
        return self.__host

    def isOccupied(self):
        return self.__Occupied

    def getStudentCounter(self):
        return self.__studentCounter

    def setRoomID(self, roomID):
        self.__roomID = roomID

    def setHost(self, host):
        self.__Host = host

    def setOccupied(self, occupied):
        self.__Occupied = occupied

    def setStudentCounter(self, studentCounter):
        self.__studentCounter = studentCounter
    
    def join(self):
        for i in range(len(self.__socketRoomList)):
            if not self.__socketRoomList[i].isFull():
                self.__socketRoomList[i].join()
            if i == len(self.__socketRoomList) - 1:
                self.__socketRoomList.append(SocketRoom(f"{self.__roomID}{chr(66 + i)}"))
                self.__socketRoomList[i + 1].join()
    
    def hostLeave(self):
        self.__socketRoomList[0].leave()

    def leave(self, sid):
        for socket_room in self.__socketRoomList:
            if socket_room.getSocketRoomPeople.get(sid):
                socket_room.leave(sid)
