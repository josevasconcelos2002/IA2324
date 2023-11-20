class Encomenda:
    def __init__(self, idnt, client, origin, destination, weight, volume, deadline=0):
        self.idnt = idnt
        self.client = client
        self.origin = origin
        self.destination = destination
        self.weight = weight
        self.volume = volume
        self.deadline = deadline
