class Room:
    def __init__(self, roomID):
        self.__roomID = roomID
        self.__host = None
        self.__Occupied = False
        self.__studentCounter = 0

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
