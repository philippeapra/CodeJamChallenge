class Load:
    def __init__(self, loadId, originLatitude, originLongitude, destinationLatitude, destinationLongitude, equipmentType, price, mileage,timestamp):
        self.loadId = loadId
        self.origin = (originLatitude, originLongitude)
        self.destination = (destinationLatitude, destinationLongitude)
        self.equipmentType = equipmentType
        self.price = price
        self.mileage = mileage
        self.timestamp= timestamp
