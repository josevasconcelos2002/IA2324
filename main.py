import tkinter as tk

import networkx as nx
import osmnx as ox

from enchaminhamento import sort_encomendas, sort_estafetas, create_sections, route, calculate_euclidean_distance

import gui as gui

from random import randint

ENCOMENDAS = []
ESTAFETAS = []
GRAPH = nx.read_gml('./dados/grafo.gml')

def main():
    root = tk.Tk()  # Fix: Tk with a capital 'T'
    app = gui.GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

