

class Truck:
    def __init__(self, truckId, positionLatitude, positionLongitude, equipType, tripLengthPreference,timestamp):
        self.truckId = truckId
        self.position = (positionLatitude, positionLongitude)
        self.equipType = equipType
        self.tripLengthPreference = tripLengthPreference
        self.timestamp =timestamp 
        self.deadhead_time_weightage=1
        self.trip_length_preference_weightage=1
        self.idleTimeWeightage= 1
        self.profit_weightage =1
        self.idleTime = 0
        

    