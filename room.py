from socketroom import SocketRoom
from flask import request
from flask_socketio import join_room, leave_room, rooms, emit
from main import MAX_STUDENT_PER_ROOM


class Room:
    __roomID: str
    __host = None
    __Occupied = False
    __studentCounter = 0
    __socketRoomList = [SocketRoom(f"{__roomID}A")]

    def __init__(self, roomID):
        self.__host = None
        self.__Occupied = False
        self.__studentCounter = 0
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

    def studentJoin(self):
        if self.__studentCounter < MAX_STUDENT_PER_ROOM:
            join_room(self.__roomID)
            for i in range(len(self.__socketRoomList)):
                if not self.__socketRoomList[i].isFull():
                    self.__socketRoomList[i].join()
                    self.__studentCounter += 1
                    return chr(65 + i)
                elif i == len(self.__socketRoomList) - 1:
                    group = f"{self.__roomID}{chr(66 + i)}"
                    self.__socketRoomList.append(SocketRoom(group))
                    join_room(group, self.__host)
                    self.__socketRoomList[i + 1].join()
                    self.__studentCounter += 1
                    return chr(66 + i)
        else:
            return None

    def hostJoin(self):
        self.__host = request.sid
        join_room(self.__roomID)
        join_room(f"{self.__roomID}A")

    def hostLeave(self):
        for room in rooms(request.sid):
            leave_room(room)
        emit("force_exit", {"Error": "False", "Msg": "Host exit"}, to=f"{self.__roomID}")

    def studentLeave(self, groupID):
        for room in self.__socketRoomList:
            if room.getSocketRoomID() == groupID:
                del room.getSocketRoomPeople()[request.sid]
                break
        self.__studentCounter -= 1
        if self.__studentCounter == 0:
            self.__init__(self.__roomID)

