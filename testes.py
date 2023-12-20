from enchaminhamento import create_routes, create_sections, sort_estafetas, sort_encomendas, route
import networkx as nx
from encomenda import Encomenda
from random import randint
from estafeta import Estafeta
from algoritmos import dijkstra
import matplotlib.pyplot as plt
import osmnx as ox

g = nx.read_gml('./dados/grafo.gml')

nodes = list(g.nodes(data=True))
origin = str(nodes[0][0])
maximum = len(nodes) - 1
encomendas = []
for i in range(30):
    encomendas.append(Encomenda(i, None, origin, nodes[randint(0, maximum)], randint(1, 2), None, 350))

estafetas = []
vehicle = 0

for i in range(15):
    if i < 5:
        vehicle = 1
    if 10 > i >= 5:
        vehicle = 2
    if i >= 10:
        vehicle = 3
    estafetas.append(Estafeta(i, vehicle))
    """
#estafetas.append(Estafeta(0, 1))
#estafetas.append(Estafeta(1, 1))

r = create_routes(g, encomendas, estafetas, dijkstra)
print(r)
total_encomendas = 0
for (s, ve), v in r.items():
    print(f'In section {s} with vehicle {ve}:')
    sec_total = 0
    for e in v:
        sec_total += 1
    print(sec_total)
    total_encomendas += sec_total
print('Encomendas no r = ' + str(total_encomendas))
    """
encomendas = sort_encomendas(g, encomendas)
estafetas = sort_estafetas(estafetas)

s = create_sections(encomendas, estafetas)

t = 0
p = 0
for k, (l, w) in s.items():
    if len(l) > 0:
        print(f"Estafeta {k}, com vehiculo {estafetas[k].vehicle.value['type']}, tem as encomendas:")
        for e in l:
            print(f"Encomenda {e.idnt}, peso {e.weight}")
            t += 1
            p += e.weight
        print(f"Com um peso total de {p}\n")
        p = 0

print(f"Para um total de {t} encomendas atribuidas")

r = route(estafetas, s, dijkstra, g)

print("VOU COMECAR AS MERDAS PESADAS MEU")

list_nodes = [int(encomenda.destination[0]) for encomenda in r[0]]

g = ox.graph_from_place('Braga, Braga', network_type="drive")

# Mudar o nome (identificação) dos nodos para conveniência de utilização apenas
# Inicialmente vêm com um número grande (osmid) como identificador. Aqui são numerados por ordem crescente
nodes, edges = ox.graph_to_gdfs(g)
node_rename_mapping = {old_node: str(new_node) for new_node, old_node in enumerate(g.nodes, start=1)}
g_un = nx.relabel_nodes(g, node_rename_mapping)

# TODO: meter isto a mostrar grafo
_, ax = ox.plot_graph(ox.project_graph(g_un), show=False, close=False)
nx.draw_networkx_nodes(g_un, pos=ox.graph_to_gdfs(g_un, edges=False).geometry.to_dict(), nodelist=list_nodes,
                       node_color='red', ax=ax)
