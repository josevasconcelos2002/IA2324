import tkinter as tk
from tkinter import ttk
import networkx as nx
from estafeta import Estafeta
from encomenda import Encomenda
import algoritmos as alg
import random


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Planet")
        self.root.geometry("500x500")

        # Adicionando a tela de boas-vindas com o logo
        self.logo_label = tk.Label(
            root, text="Health Planet", font=("Helvetica", 24))
        self.logo_label.pack(pady=50)

        # Adicionando um botão para continuar após o clique do usuário
        self.continuar_btn = ttk.Button(
            root, text="Clique para Continuar", command=self.mostrar_menu)
        self.continuar_btn.pack(pady=20)

        # Inicialmente, ocultar o menu de escolha do algoritmo
        self.menu_frame = ttk.Frame(root)
        self.menu_frame.pack_forget()

        # Configurando o menu
        self.label = ttk.Label(self.menu_frame, text="Escolha o algoritmo:")
        self.label.pack(pady=10)

        self.algoritmo_var = tk.StringVar()

        self.radio_dfs = ttk.Radiobutton(
            self.menu_frame, text="DFS", variable=self.algoritmo_var, value="dfs")
        self.radio_dfs.pack()

        self.radio_bfs = ttk.Radiobutton(
            self.menu_frame, text="BFS", variable=self.algoritmo_var, value="bfs")
        self.radio_bfs.pack()

        self.radio_custo_uniforme = ttk.Radiobutton(
            self.menu_frame, text="Custo Uniforme", variable=self.algoritmo_var, value="custo_uniforme")
        self.radio_custo_uniforme.pack()

        self.btn_executar = ttk.Button(
            self.menu_frame, text="Executar", command=self.executar_algoritmo)
        self.btn_executar.pack(pady=10)

        self.btn_sair = ttk.Button(
            self.menu_frame, text="Sair", command=root.destroy)
        self.btn_sair.pack(pady=10)

    def mostrar_menu(self):
        # Esconder a tela de boas-vindas
        self.logo_label.pack_forget()
        self.continuar_btn.pack_forget()

        # Mostrar o menu de escolha do algoritmo
        self.menu_frame.pack(pady=50)

    def executar_algoritmo(self):
        escolha = self.algoritmo_var.get()

        if escolha == "dfs":
            algorithm = alg.dfs
        elif escolha == "bfs":
            algorithm = alg.bfs
        elif escolha == "custo_uniforme":
            algorithm = alg.custo_uniforme
        else:
            print("Escolha inválida.")
            return

        g, edges = build_graph()
        est1 = Estafeta(1, 1)
        enc1 = Encomenda(1, "Fabio", "3", "10", 3, 10)

        encomendas = [
            [i, f"Cliente_{i}", str(random.randint(1, 40)), str(
                random.randint(1, 40)), random.randint(1, 10), random.randint(1, 10)]
            for i in range(1, 101)
        ]

        visited, path, cost = algorithm(g, enc1.origin, enc1.destination)

        print(f"Resultado do algoritmo escolhido:")
        print(f"Visited: {visited}")
        print(f"Path: {path}")
        print(f"Cost: {cost} kms")


def build_graph():
    nodes_info = {}
    with open("./dados/freguesias.txt", "r") as file:
        i = 1
        for line in file:
            freguesia = line.strip()
            nodes_info.update({str(i): {"nome": freguesia, "ocupado": False}})
            i += 1

    edges = []
    with open("./dados/arestas.txt", "r") as file:
        for line in file:
            origem, destino, distancia = line.split(";")
            edges.append((origem, destino, {"distance": float(distancia)}))

    g = nx.Graph()
    g.add_nodes_from(nodes_info.keys())
    g.add_edges_from(edges)

    return g, edges


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
