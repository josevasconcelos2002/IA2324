import tkinter as tk
from tkinter import ttk
import networkx as nx
from estafeta import Estafeta
from encomenda import Encomenda
from enchaminhamento import create_sections, sort_estafetas, sort_encomendas, route
import matplotlib.pyplot as plt
import osmnx as ox
import algoritmos as alg
import random    

g = nx.read_gml('./dados/grafo.gml')

nodes = list(g.nodes(data=True))
origin = str(nodes[0][0])
maximum = len(nodes) - 1
encomendas = []
for i in range(30):
    encomendas.append(Encomenda(
        i, None, origin, nodes[random.randint(0, maximum)], random.randint(1, 2), None, 350))

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

encomendas = [
    [i, f"Cliente_{i}", str(random.randint(1, 40)), str(
        random.randint(1, 40)), random.randint(1, 10), random.randint(1, 10)]
    for i in range(1, 101)
]