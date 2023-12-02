from encomenda import Encomenda
from random import randint
from estafeta import Estafeta
from enchaminhamento import create_sections, combine_by_weight, route
from algoritmos import dijkstra
import networkx as nx

g = nx.read_gml('./dados/grafo.gml')

list_encomendas = []
nodes = list(g.nodes(data=True))
origin = str(nodes[0][0])
maximum = len(nodes) - 1
for i in range(1, 11):
    list_encomendas.append(Encomenda(i, None, origin, nodes[randint(0, maximum)], randint(1, 30), None, 999999))

list_estafetas = []
vehicle = 0
for i in range(0, 16):
    if i < 5:
        vehicle = 1
    if 10 > i > 5:
        vehicle = 2
    if i > 10:
        vehicle = 3
    list_estafetas.append(Estafeta(i, vehicle))

sec = create_sections(list_encomendas)

gsec = combine_by_weight(sec)
r = route(list_estafetas, sec, gsec, dijkstra, g, origin)
print(r)
total_encomendas = 0
for k, v in sec.items():
    print('In section ' + str(k) + ' there are ' + str(len(v)) + ' encomendas')
for (s, ve), v in r.items():
    print(f'In section {s} with vehicle {ve}:')
    sec_total = 0
    for e in v:
        sec_total += 1
    print(sec_total)
    total_encomendas += sec_total
print('Encomendas no r = ' + str(total_encomendas))
