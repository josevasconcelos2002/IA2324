class Encomenda:
    def __init__(self, idnt, client, destination, weight, deadline=0):
        self.idnt = idnt
        self.client = client
        self.weight = weight
        self.destination = destination
        self.deadline = deadline

    def criar_encomenda(self, idnt, client, destination, weigth, deadline=0):
        encomenda = Encomenda(idnt, client, destination, weigth, deadline)
        return encomenda