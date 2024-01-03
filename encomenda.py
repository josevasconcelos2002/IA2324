import networkx as nx


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
    
    def nodos_por_rua(rua, GRAPH):
        nodos_encontrados = []

        for nodo_id, nodo_atributos in GRAPH.nodes(data=True):
            if 'name' in nodo_atributos and nodo_atributos['name'] == rua:
                if 'source' in nodo_atributos and 'target' in nodo_atributos:
                    nodos_encontrados.extend([nodo_atributos['source'], nodo_atributos['target']])

        return nodos_encontrados