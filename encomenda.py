class Encomenda:
    def __init__(self, idnt, client, origin, destination, deadline=0):
        self.idnt = idnt
        self.client = client
        self.origin = origin
        self.destination = destination
        self.deadline = deadline

    def criar_encomenda(idnt, client, destination, deadline=0):
        origin = input(f"Digite a origem da encomenda: ")

        encomenda = Encomenda(idnt, client, origin, destination, deadline)
    
        return encomenda