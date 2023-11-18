class Encomenda:
    def __init__(self, idnt, cliente, peso, volume, deadline=0):
        self.idnt = idnt
        self.cliente = cliente
        self.peso = peso
        self.volume = volume
        self.deadline = deadline
