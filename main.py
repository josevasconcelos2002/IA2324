import tkinter as tk

import networkx as nx

import gui as gui

ENCOMENDAS = []
ESTAFETAS = []
GRAPH = nx.read_gml('./dados/grafo.gml')

def main():
    root = tk.Tk()  # Fix: Tk with a capital 'T'
    app = gui.GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()