class Encomenda:
    def __init__(self, idnt, client, weight, volume, deadline=0):
        self.idnt = idnt
        self.client = client
        self.weigth = weight
        self.volume = volume
        self.deadline = deadline
