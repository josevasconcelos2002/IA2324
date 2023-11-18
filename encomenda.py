class Encomenda:
    def __init__(self, idnt, client, weight, volume, deadline=0):
        self.idnt = idnt
        self.cliente = client
        self.peso = weight
        self.volume = volume
        self.deadline = deadline
