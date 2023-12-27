class Encomenda:
    def __init__(self, idnt, client, destination, weigth, deadline=0):
        self.idnt = idnt
        self.client = client
        self.destination = destination
        self.weigth = weigth

    def criar_encomenda(idnt, client, destination, weigth, deadline=0):
        origin = input(f"Digite a origem da encomenda: ")

        encomenda = Encomenda(idnt, client, origin, destination, weigth, deadline)
    
        return encomenda