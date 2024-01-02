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
    
    def nodos_por_rua(rua):
        nodos_encontrados = []
        
        grafo = nx.read_gml('./dados/grafo.gml')

        # Iterar sobre todos os nodos
        for nodo_id, nodo_atributos in grafo.nodes(data=True):
            if 'name' in nodo_atributos and nodo_atributos['name'] == rua:
                nodos_encontrados.append(nodo_atributos['source'])
                nodos_encontrados.append(nodo_atributos['target'])

        return nodos_encontrados