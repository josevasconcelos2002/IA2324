from enum import Enum


class Vehicle(Enum):
    CAR = {"type": 1, "speed": 50, "max_weight": 100, "radius": 200}
    BIKE = {"type": 2, "speed": 35, "max_weight": 20, "radius": 150}
    BICYCLE = {"type": 3, "speed": 10, "max_weight": 5, "radius": 75}


class Estafeta:
    def __init__(self, idnt, vehicle_type, rating=5):
        self.idnt = idnt
        self.vehicle = next(member for member in Vehicle if member.value["type"] == vehicle_type)
        self.deliveries = 1
        self.rating = rating

    def rate(self, rating):
        self.deliveries += 1
        self.rating = round((self.rating + rating) / self.deliveries, 2)
