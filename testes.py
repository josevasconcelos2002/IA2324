import sys

from enchaminhamento import create_sections, sort_estafetas, sort_encomendas, route
import networkx as nx
from encomenda import Encomenda
from random import randint
from estafeta import Estafeta
from algoritmos import dijkstra, bfs, dfs, iddfs, dfs_limit, bidirectional, greedy_search, astar_search
import osmnx as ox
import time

g = nx.read_gml('./dados/grafo.gml')

nodes = list(g.nodes(data=True))
origin = str(nodes[0][0])
maximum = len(nodes) - 1
encomendas = []
for i in range(30):
    encomendas.append(Encomenda(
        i, None, origin, nodes[randint(0, maximum)], randint(1, 2), None, 350))

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
start_time = time.time()
s = create_sections(encomendas, estafetas)
"""
t = 0
p = 0
for k, (l, w) in s.items():
    if len(l) > 0:
        print(
            f"Estafeta {k}, com vehiculo {estafetas[k].vehicle.value['type']}, tem as encomendas:")
        for e in l:
            print(f"Encomenda {e.idnt}, peso {e.weight}")
            t += 1
            p += e.weight
        print(f"Com um peso total de {p}\n")
        p = 0

print(f"Para um total de {t} encomendas atribuidas")
"""
algoritmo = dijkstra
r, late = route(estafetas, s, algoritmo, g)
total_time = time.time() - start_time
print(r)
print("Realizou route")

for section, route in r.items():
    if len(route) == 1:
        ox.plot_graph_route(g, route[0], route_color='yellow', route_linewidth=6, node_size=0, route_alpha=1,
                            show=False, save=True, filepath=f"./routes/section_{section}.png")
    else:
        ox.plot_graph_routes(g, route, route_colors='yellow', route_linewidth=6, node_size=0, route_alpha=1,
                            show=False, save=True, filepath=f"./routes/section_{section}.png")

for estafeta, (rating, late_encomendas, n_encomendas) in late.items():
    with open(f"./routes/{estafeta}_relatorio.txt", 'w') as f:
        lines = [f"Estafeta: {estafeta}\n", f"Numero de encomendas: {n_encomendas}\n"
            , f"Rating: {format(rating / n_encomendas, '.1f')}\n", 'Encomendas atrasadas:\n']
        for enc, time in late_encomendas.items():
            lines.append(f"Encomenda {enc}: {time}\n")
        lines.append(f"\n\nTempo de processamento: {total_time} segundos")
        f.writelines(lines)

with open(f"./routes/informacao.txt", 'w') as f:
    f.writelines([f"Algoritmo utilizado: {algoritmo.__name__}\n", f"Tempo de processamento: {format(total_time, '.2f')} s"])