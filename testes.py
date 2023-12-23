from enchaminhamento import create_routes, create_sections, sort_estafetas, sort_encomendas, route
import networkx as nx
from encomenda import Encomenda
from random import randint
from estafeta import Estafeta
from algoritmos import dijkstra, bfs
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
print(r)
print("Realizou route")

# = ['b' if (u == 'ORIGIN') else 'yellow' for u, v, k in g.edges(keys=True)]
#ox.plot_graph_routes(g, r[0], route_linewidth=6, node_size=0, route_alpha=1, node_color=node_color)
for section, route in r.items():
    ox.plot_graph_routes(g, route, route_colors='yellow', route_linewidth=6, node_size=0, route_alpha=1,
                         show=False, save=True, filepath=f"./routes/section_{section}.png")