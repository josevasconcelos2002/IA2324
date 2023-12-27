import tkinter as tk
from tkinter import ttk
import algoritmos as alg
import networkx as nx
from estafeta import Estafeta
from encomenda import Encomenda
import random
import logging


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Planet")
        self.root.geometry("500x500")
        self.current_frame = self.root
        self._estafetas = []
        self._encomendas = []

        self.setup_tela_boas_vindas()
        self.setup_menu_inicial()

        # Adiciona a tela de boas-vindas com o logo e botão para continuar

    def setup_tela_boas_vindas(self):
        self.logo_label = tk.Label(self.root, text="Health Planet", font=("Helvetica", 24))
        self.logo_label.pack(pady=50)

        self.continuar_btn = ttk.Button(self.root, text="Clique para Continuar", command=self.show_menu_inicial)
        self.continuar_btn.pack(pady=20)

    # Frame para o menu inicial
    def show_menu_inicial(self):
        self.logo_label.pack_forget()
        self.continuar_btn.pack_forget()
        if self.current_frame != self.root:
            self.current_frame.pack_forget()

        self.current_frame = self.frame_menu_inicial
        self.setup_menu_inicial()
        self.frame_menu_inicial.pack(pady=50)

    # Configurador de menu inicial
    def setup_menu_inicial(self):
        self.frame_menu_inicial = ttk.Frame(self.root)

        self.btn_criar_estafeta = ttk.Button(self.frame_menu_inicial, text='Criar estafeta',
                                             command=self.show_menu_estafeta)
        self.btn_criar_estafeta.pack(pady=10)
        
        self.btn_criar_encomenda = ttk.Button(self.frame_menu_inicial, text='Criar encomenda',
                                             command=self.show_menu_encomenda)
        self.btn_criar_encomenda.pack(pady=10)

        self.btn_algoritmos = ttk.Button(self.frame_menu_inicial, text="Executar algoritmos",
                                         command=self.show_menu_algoritmos)
        self.btn_algoritmos.pack(pady=20)

    # Frame para o menu de escolha dos algoritmos
    def show_menu_algoritmos(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_algoritmos
        self.frame_algoritmos.pack(pady=50)

    # Configurador do menu de escolha dos algoritmos
    def setup_menu_algoritmos(self):
        self.frame_algoritmos = ttk.Frame(self.root)

        self.label = ttk.Label(self.frame_algoritmos, text="Escolha o algoritmo:")
        self.label.pack(pady=10)

        self.algoritmo_var = tk.StringVar()

        self.radio_dfs = ttk.Radiobutton(self.frame_algoritmos, text="DFS", variable=self.algoritmo_var, value="dfs")
        self.radio_dfs.pack()

        self.radio_bfs = ttk.Radiobutton(self.frame_algoritmos, text="BFS", variable=self.algoritmo_var, value="bfs")
        self.radio_bfs.pack()

        self.radio_dijkstra = ttk.Radiobutton(self.frame_algoritmos, text="Dijkstra", variable=self.algoritmo_var,
                                              value="dijkstra")
        self.radio_dijkstra.pack()

        self.radio_iddfs = ttk.Radiobutton(self.frame_algoritmos, text="IDDFS", variable=self.algoritmo_var,
                                           value="iddfs")
        self.radio_iddfs.pack()

        self.radio_bidirectional = ttk.Radiobutton(self.frame_algoritmos, text="Bidirectional",
                                                   variable=self.algoritmo_var, value="bidirectional")
        self.radio_bidirectional.pack()

        self.radio_greedy = ttk.Radiobutton(self.frame_algoritmos, text="Greedy",
                                                   variable=self.algoritmo_var, value="greedy_search")
        self.radio_greedy.pack()

        self.radio_astar = ttk.Radiobutton(self.frame_algoritmos, text="A*",
                                                   variable=self.algoritmo_var, value="astar_search")
        self.radio_astar.pack()

        self.btn_executar = ttk.Button(self.frame_algoritmos, text="Executar", command=self.executar_algoritmo)
        self.btn_executar.pack(pady=10)

        self.btn_sair_algoritmos = ttk.Button(self.frame_algoritmos, text="Sair", command=self.show_menu_inicial)
        self.btn_sair_algoritmos.pack(pady=10)

    # Este método deve passar para dentro da class algoritmos e ser importado
    def executar_algoritmo(self):
        escolha = self.algoritmo_var.get()

        if escolha not in ["dfs", "bfs", "dijkstra", "iddfs", "bidirectional", "greedy_searcj", "astar_search"]:
            logging.warning("Escolha inválida.")
            return

        algorithm = getattr(alg, escolha, None)
        if algorithm is None or not callable(algorithm):
            logging.warning(f"Algoritmo {escolha} não encontrado.")
            return

        g = nx.read_gml('./dados/grafo.gml')
        est1 = Estafeta(1, 1)
        enc1 = Encomenda(1, "Fabio", "3", "11", 3, 10)

        encomendas = [
            [i, f"Cliente_{i}", str(random.randint(1, 40)), str(
                random.randint(1, 40)), random.randint(1, 10), random.randint(1, 10)]
            for i in range(1, 101)
        ]

        visited, path, cost = algorithm(g, enc1.origin, enc1.destination)

        print(f"Resultado do algoritmo escolhido:")
        print(f"Visited: {visited}")
        print(f"Caminho: {path}")
        print(f"Custo: {cost}")

    # Configurador do menu de escolha dos algoritmos
    def show_menu_estafeta(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_estafeta
        self.clean_estafeta_vars()
        self.frame_estafeta.pack(pady=50)

    # Configurador do menu de estfetas
    def setup_menu_estafeta(self):
        self.frame_estafeta = ttk.Frame(self.root)

        self.enc_label = ttk.Label(self.frame_estafeta, text="Estafeta:")
        self.enc_label.pack(pady=10)

        self.var_estafeta = tk.StringVar()

        self.text_estafeta = tk.Text(self.frame_estafeta, height=1, width=20)
        self.text_estafeta.pack(pady=10)

        self.var_vehiculo = tk.IntVar()

        self.radio_bicycle = ttk.Radiobutton(self.frame_estafeta, text="Bicicleta", variable=self.var_vehiculo, value=1)
        self.radio_bicycle.pack()

        self.btn_criar_estafeta = ttk.Button(self.frame_estafeta, text="Criar", command=self.save_estafeta)
        self.btn_criar_estafeta.pack()

        self.btn_sair_estafeta = ttk.Button(self.frame_estafeta, text="Sair", command=self.show_menu_inicial)
        self.btn_sair_estafeta.pack(pady=10)

    def save_estafeta(self):
        vehiculo = self.var_vehiculo.get()
        nome = self.text_estafeta.get(1.0, "end-1c")
        if vehiculo != 0 and nome != '':
            self._estafetas.append(Estafeta(nome, vehiculo))
            self.clean_estafeta_vars()

    def clean_estafeta_vars(self):
        self.text_estafeta.delete("1.0", "end")
        self.var_vehiculo.set(0)


    def show_menu_encomenda(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_encomenda
        self.clean_encomenda_vars()
        self.frame_encomenda.pack(pady=50)

    def setup_menu_encomenda(self):
        self.frame_encomenda = ttk.Frame(self.root)

        self.enc_label = ttk.Label(self.frame_encomenda, text="Encomenda:")
        self.enc_label.pack(pady=10)

        self.var_encomenda = tk.StringVar()

        self.text_encomenda = tk.Text(self.frame_encomenda, height=1, width=20)
        self.text_encomenda.pack(pady=10)

        self.btn_criar_encomenda = ttk.Button(self.frame_encomenda, text="Criar", command=self.save_encomenda)
        self.btn_criar_encomenda.pack()

        self.btn_sair_encomenda = ttk.Button(self.frame_encomenda, text="Sair", command=self.show_menu_inicial)
        self.btn_sair_encomenda.pack(pady=10)

    def save_encomenda(self):
        Idnt = self.text_encomenda.get(1.0, "end-1c")
        Client = self.text_encomenda.get(1.0, "end-1c")
        Origem = self.text_encomenda.get(1.0, "end-1c")
        Destino = self.text_encomenda.get(1.0, "end-1c")
        if Client != '' and Origem != '' and Destino != '':
            self._encomendas.append(Encomenda(Idnt, Client, Origem, Destino))
            self.clean_encomenda_vars()

    def clean_encomenda_vars(self):
        self.text_encomenda.delete("1.0", "end")



'''
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Planet")
        self.root.geometry("500x500")
        self.current_frame = self.root
        self._estafetas = []

        # Adiciona a tela de boas-vindas com o logo

        self.logo_label = tk.Label(
            self.root, text="Health Planet", font=("Helvetica", 24))
        self.logo_label.pack(pady=50)

        # Adicionando um botão para continuar após o clique do usuário
        self.continuar_btn = ttk.Button(
            self.root, text="Clique para Continuar", command=self.mostrar_menu)
        self.continuar_btn.pack(pady=20)

        # Frame para o menu inicial
        self.frame_menu_inicial = ttk.Frame(root)
        self.frame_menu_inicial.pack_forget()

        # Botões para criar estafeta e executar algoritmos
        self.btn_criar_estafeta = ttk.Button(
            self.frame_menu_inicial, text='Criar estafeta', command=self.mostrar_estafeta)
        self.btn_criar_estafeta.pack(pady=10)

        self.btn_algoritmos = ttk.Button(
            self.frame_menu_inicial, text="Executar algoritmos", command=self.mostrar_algoritmos)
        self.btn_algoritmos.pack(pady=20)

        # Inicialmente, ocultar o menu de escolha do algoritmo
        # Frame para escolher algoritmo
        self.frame_algoritmos = ttk.Frame(root)
        self.frame_algoritmos.pack_forget()

        # Configurando o menu
        self.label = ttk.Label(self.frame_algoritmos, text="Escolha o algoritmo:")
        self.label.pack(pady=10)

        self.algoritmo_var = tk.StringVar()

        # Botões de seleção de algoritmo
        self.radio_dfs = ttk.Radiobutton(
            self.frame_algoritmos, text="DFS", variable=self.algoritmo_var, value="dfs")
        self.radio_dfs.pack()

        self.radio_bfs = ttk.Radiobutton(
            self.frame_algoritmos, text="BFS", variable=self.algoritmo_var, value="bfs")
        self.radio_bfs.pack()

        self.radio_dijkstra = ttk.Radiobutton(
            self.frame_algoritmos, text="Dijkstra", variable=self.algoritmo_var, value="dijkstra")
        self.radio_dijkstra.pack()

        self.radio_iddfs = ttk.Radiobutton(
            self.frame_algoritmos, text="IDDFS", variable=self.algoritmo_var, value="iddfs")
        self.radio_iddfs.pack()

        self.radio_bidirectional = ttk.Radiobutton(
            self.frame_algoritmos, text="Bidirectional", variable=self.algoritmo_var, value="bidirectional")
        self.radio_bidirectional.pack()

        # Botões para executar algoritmo e sair
        self.btn_executar = ttk.Button(
            self.frame_algoritmos, text="Executar", command=self.executar_algoritmo)
        self.btn_executar.pack(pady=10)

        self.btn_sair_algoritmos = ttk.Button(
            self.frame_algoritmos, text="Sair", command=self.mostrar_menu)
        self.btn_sair_algoritmos.pack(pady=10)

        # Frame para criar estafeta
        self.frame_estafeta = ttk.Frame(root)
        self.frame_estafeta.pack_forget()

        self.enc_label = ttk.Label(self.frame_estafeta, text="Estafeta:")
        self.enc_label.pack(pady=10)

        self.var_estafeta = tk.StringVar()

        self.text_estafeta = tk.Text(self.frame_estafeta, height=1, width=20)
        self.text_estafeta.pack(pady=10)

        self.var_vehiculo = tk.IntVar()

        # Botões de seleção de veículo
        self.radio_bicycle = ttk.Radiobutton(
            self.frame_estafeta, text="Bicicleta", variable=self.var_vehiculo, value=1)
        self.radio_bicycle.pack()

        self.radio_bike = ttk.Radiobutton(
            self.frame_estafeta, text="Mota", variable=self.var_vehiculo, value=2)
        self.radio_bike.pack()

        self.radio_car = ttk.Radiobutton(
            self.frame_estafeta, text="Carro", variable=self.var_vehiculo, value=3)
        self.radio_car.pack()

        # Botões para criar estafeta e sair
        self.btn_criar_estafeta = ttk.Button(
            self.frame_estafeta, text="Criar", command=self.save_estafeta)
        self.btn_criar_estafeta.pack()

        self.btn_sair_estafeta = ttk.Button(
            self.frame_estafeta, text="Sair", command=self.mostrar_menu)
        self.btn_sair_estafeta.pack(pady=10)

    def mostrar_menu(self):
        # Esconder a tela de boas-vindas
        self.logo_label.pack_forget()
        self.continuar_btn.pack_forget()
        if self.current_frame != self.root:
            self.current_frame.pack_forget()

        self.current_frame = self.frame_menu_inicial
        # Mostrar o menu de escolha do algoritmo
        self.frame_menu_inicial.pack(pady=50)

    # Função para mostrar a interface de escolha de algoritmo
    def mostrar_algoritmos(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_algoritmos
        self.frame_algoritmos.pack(pady=50)

    def executar_algoritmo(self):
        escolha = self.algoritmo_var.get()

        if escolha not in ["dfs", "bfs", "dijkstra", "iddfs", "bidirectional"]:
            logging.warning("Escolha inválida.")
            return

        algorithm = getattr(alg, escolha, None)
        if algorithm is None or not callable(algorithm):
            logging.warning(f"Algoritmo {escolha} não encontrado.")
            return

        g = nx.read_gml('./dados/grafo.gml')
        est1 = Estafeta(1, 1)
        enc1 = Encomenda(1, "Fabio", "3", "11", 3, 10)

        encomendas = [
            [i, f"Cliente_{i}", str(random.randint(1, 40)), str(
                random.randint(1, 40)), random.randint(1, 10), random.randint(1, 10)]
            for i in range(1, 101)
        ]

        visited, path, cost = algorithm(g, enc1.origin, enc1.destination)

        print(f"Resultado do algoritmo escolhido:")
        print(f"Visited: {visited}")
        print(f"Caminho: {path}")
        print(f"Custo: {cost}")

    def mostrar_estafeta(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_estafeta
        self.clean_estafeta_vars()
        self.frame_estafeta.pack(pady=50)

    def save_estafeta(self):
        vehiculo = self.var_vehiculo.get()
        nome = self.text_estafeta.get(1.0, "end-1c")
        if vehiculo != 0 and nome != '':
            ESTAFETAS.append(Estafeta(nome, vehiculo))
            self.clean_estafeta_vars()

    def clean_estafeta_vars(self):
        self.text_estafeta.delete("1.0", "end")
        self.var_vehiculo.set(0)
'''