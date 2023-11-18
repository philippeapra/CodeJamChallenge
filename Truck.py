

class Truck:
    def __init__(self, truckId, positionLatitude, positionLongitude, equipType, tripLengthPreference,timestamp):
        self.truckId = truckId
        self.position = (positionLatitude, positionLongitude)
        self.equipType = equipType
        self.tripLengthPreference = tripLengthPreference
        self.timestamp =timestamp 
        self.idleTime = 0
        

    