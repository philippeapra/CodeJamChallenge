from CustomEncoder import *
import pprint

class Truck:
    def __init__(self, truckId, positionLatitude, positionLongitude, equipType, tripLengthPreference):
        self.truckId = truckId
        self.position = (positionLatitude, positionLongitude)
        self.equipType = equipType
        self.tripLengthPreference = tripLengthPreference

    def __str__(self):
        truckDict={}
        truckDict[self.truckId] = self.truckId
        truckDict[self.position] = self.position
        truckDict[self.equipType] = self.equipType
        truckDict[self.tripLengthPreference] = self.tripLengthPreference
        return json.dumps(truckDict, indent=4)