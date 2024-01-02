from random import randint
import tkinter as tk
from tkinter import ttk
import time
from tkinter import StringVar, Entry


import algoritmos as alg
import networkx as nx
import osmnx as ox
from estafeta import Estafeta
from encomenda import Encomenda
from enchaminhamento import sort_encomendas, sort_estafetas, create_sections, route, calculate_euclidean_distance


ENCOMENDAS = []
ESTAFETAS = []
GRAPH = nx.read_gml('./dados/grafo.gml')

def get_vehicle(est_id, list_e):
    estafeta = None
    for est in list_e:
        if est.idnt == str(est_id):
            estafeta = est
            break
    if estafeta.vehicle.value['type'] == 1:
        v = 'Carro'
    elif estafeta.vehicle.value['type'] == 2:
        v = 'Mota'
    else:
        v = 'Bicicleta'
    return v

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Planet")
        self.root.geometry("500x560")
        self.current_frame = self.root


        self.setup_tela_boas_vindas()
        self.setup_menu_inicial()
        
        #self.var_destino_entry = StringVar()
        #self.var_destino_entry.trace_add("write", self.atualizar_hipoteses_destino)
        
        self.setup_menu_encomenda()

        self.setup_menu_estafeta()

        self.setup_menu_algoritmos()

        self.setup_gerar()


    def setup_tela_boas_vindas(self):
        self.logo_label = tk.Label(self.root, text="Health Planet", font=("Helvetica", 24))
        self.logo_label.pack(pady=50)

        self.continuar_btn = ttk.Button(self.root, text="Clique para Continuar", command=self.mostrar_menu_inicial)
        self.continuar_btn.pack(pady=20)

    def mostrar_menu_inicial(self):
        self.logo_label.pack_forget()
        self.continuar_btn.pack_forget()
        if self.current_frame != self.root:
            self.current_frame.pack_forget()

        self.current_frame = self.frame_menu_inicial
        self.frame_menu_inicial.pack(pady=50)

    def setup_menu_inicial(self):
        self.frame_menu_inicial = ttk.Frame(self.root)

        self.btn_criar_estafeta = ttk.Button(
            self.frame_menu_inicial, text='Criar estafeta',command=self.mostrar_menu_estafeta)
        self.btn_criar_estafeta.pack(pady=10)

        self.btn_criar_encomenda = ttk.Button(
            self.frame_menu_inicial, text='Criar encomenda', command=self.mostrar_menu_encomenda)
        self.btn_criar_encomenda.pack(pady=20)

        self.btn_gerar_automatico = ttk.Button(
            self.frame_menu_inicial, text='Gerar automaticamente', command=self.mostar_gerar)
        self.btn_gerar_automatico.pack(pady=20)

        self.btn_algoritmos = ttk.Button(
            self.frame_menu_inicial, text="Executar algoritmos", command=self.mostrar_menu_algoritmos)
        self.btn_algoritmos.pack(pady=30)

    def mostrar_menu_algoritmos(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_algoritmos
        self.frame_algoritmos.pack(pady=50)

    def setup_menu_algoritmos(self):
        
        self.frame_algoritmos = ttk.Frame(self.root)

        self.label = ttk.Label(self.frame_algoritmos, text="Escolha o algoritmo:")
        self.label.pack(pady=10)

        self.algoritmo_var = tk.StringVar()

        algorithms = ["dfs", "bfs", "dijkstra", "iddfs", "bidirectional", "greedy_search", "astar_search"]

        for algo in algorithms:
            ttk.Radiobutton(self.frame_algoritmos, text=algo.capitalize(), variable=self.algoritmo_var, value=algo).pack()

        self.btn_executar = ttk.Button(self.frame_algoritmos, text="Executar", command=self.executar_algoritmo)
        self.btn_executar.pack(pady=10)

        self.btn_sair_algoritmos = ttk.Button(self.frame_algoritmos, text="Sair", command=self.mostrar_menu_inicial)
        self.btn_sair_algoritmos.pack(pady=10)

    def executar_algoritmo_automatico(self):
        n_estafetas = self.text_n_estafetas.get(1.0, "end-1c")
        n_encomendas = self.text_n_encomendas.get(1.0, "end-1c")
        if not n_estafetas.isdigit() or not n_encomendas.isdigit():
            return
        n_estafetas = int(n_estafetas)
        n_encomendas = int(n_encomendas)

        #Tenta criar uma distribuição equilibrada de estafetas por vehiculo
        estafetas = []
        third, remainder = divmod(n_estafetas, 3)
        vehicles = [3] * third + [2] * third + [1] * third
        for _ in range(remainder):
            vehicles.append(1)
        for i in range(n_estafetas):
            estafetas.append(Estafeta(str(i), vehicles[i]))

        encomendas = []
        nodes = GRAPH.nodes(data=True)
        maximum = len(nodes) - 1
        o_x = nodes['ORIGIN']['x']
        o_y = nodes['ORIGIN']['y']
        nodes_l = list(nodes)
        for i in range(n_encomendas):
            destination = nodes_l[randint(0, maximum)]
            while destination[0] == 5379:
                destination = nodes_l[randint(0, maximum)]
            dest_node = nodes[destination[0]]
            #A deadline é calculada através da distancia euclidiana até à origem
            o_dist = calculate_euclidean_distance(o_x, o_y, dest_node['x'], dest_node['y'])
            deadline = (o_dist / 100) * 3600
            encomendas.append(Encomenda(
                i, None, destination, randint(1, 2), deadline))
        self.executar_algoritmo(estafetas, encomendas, self.algoritmo_gerar_var.get())

    def executar_algoritmo(self, estafetas=None, encomendas=None, escolha=''):
        if encomendas is None:
            encomendas = ENCOMENDAS
        if estafetas is None:
            estafetas = ESTAFETAS
        if len(encomendas) == 0 or len(estafetas) == 0:
            return

        if escolha == '':
            escolha = self.algoritmo_var.get()

        if escolha == "dfs":
            algorithm = alg.dfs
        elif escolha == "bfs":
            algorithm = alg.bfs
        elif escolha == "dijkstra":
            algorithm = alg.dijkstra
        elif escolha == "iddfs":
            algorithm = alg.iddfs
        elif escolha == "bidirectional":
            algorithm = alg.bidirectional
        elif escolha == "greedy_search":
            algorithm = alg.greedy_search
        elif escolha == "astar_search":
            algorithm = alg.astar_search    
        else:
            print("Escolha inválida.")
            return

        print("A executar...")
        encomendas = sort_encomendas(GRAPH, encomendas)
        estafetas = sort_estafetas(estafetas)
        start_time = time.time()
        s = create_sections(encomendas, estafetas)
        print('Secções criadas')

        r, late = route(estafetas, s, algorithm, GRAPH)
        total_time = time.time() - start_time
        print("Rotas calculadas")
        for estafeta, (t_rating, late_encomendas, n_encomendas) in late.items():
            with open(f"Resultados/Estafetas/{estafeta}_relatorio.txt", 'w') as f:
                lines = [f"Estafeta: {estafeta}\n", f"Vehículo: {get_vehicle(estafeta, estafetas)}\n",
                         f"Numero de encomendas: {n_encomendas}\n"
                    , f"Rating: {format(t_rating / n_encomendas, '.2f')}\n", 'Encomendas atrasadas:\n']
                for enc, (delay, rating) in late_encomendas.items():
                    lines.append(f"Encomenda {enc}: {self.seconds_to_hours_minutes(delay)} (rating: {rating})\n")
                f.writelines(lines)

        for section, v in r.items():
            rota = v['path']
            custo = v['cost']
            if len(rota) == 1:
                ox.plot_graph_route(GRAPH, rota[0], route_color='yellow', route_linewidth=6, node_size=0, route_alpha=1,
                                    show=False, save=True, filepath=f"Resultados/Rotas/section_{section}.png")
            else:
                ox.plot_graph_routes(GRAPH, rota, route_colors='yellow', route_linewidth=6, node_size=0, route_alpha=1,
                                     show=False, save=True, filepath=f"Resultados/Rotas/section_{section}.png")
            with open(f"Resultados/Estafetas/{section}_relatorio.txt", 'a') as f:
                lines = [f"\n\nCusto total: {custo}\n", 'Rotas:']
                for r in rota:
                    lines.append(str(r))
                f.writelines(lines)

        with open(f"Resultados/informacao.txt", 'w') as f:
            f.writelines([f"Algoritmo utilizado: {escolha}\n",
                          f"Tempo de processamento: {format(total_time, '.2f')} s"])
        print("Execução completa. Verifique os dados na pasta Resultados.")
    
    def mostrar_menu_estafeta(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_estafeta
        self.clean_estafeta_vars()
        self.frame_estafeta.pack(pady=50)

    def setup_menu_estafeta(self):
        self.frame_estafeta = ttk.Frame(self.root)

        ttk.Label(self.frame_estafeta, text="Estafeta:").pack(pady=10)

        self.var_estafeta = tk.StringVar()

        self.text_estafeta = tk.Text(self.frame_estafeta, height=1, width=20)
        self.text_estafeta.pack(pady=10)

        self.var_vehiculo = tk.IntVar()

        self.radio_bicycle = ttk.Radiobutton(
            self.frame_estafeta, text="Bicicleta", variable=self.var_vehiculo, value=1)
        self.radio_bicycle.pack()

        self.radio_bike = ttk.Radiobutton(
            self.frame_estafeta, text="Mota", variable=self.var_vehiculo, value=2)
        self.radio_bike.pack()

        self.radio_car = ttk.Radiobutton(
            self.frame_estafeta, text="Carro", variable=self.var_vehiculo, value=3)
        self.radio_car.pack()

        self.btn_criar_estafeta = ttk.Button(
            self.frame_estafeta, text="Criar", command=self.save_estafeta)
        self.btn_criar_estafeta.pack()

        self.btn_sair_estafeta = ttk.Button(
            self.frame_estafeta, text="Sair", command=self.mostrar_menu_inicial)
        self.btn_sair_estafeta.pack(pady=10)

    def save_estafeta(self):
        vehiculo = self.var_vehiculo.get()
        nome = self.text_estafeta.get(1.0, "end-1c")
        if vehiculo != 0 and nome != '':
            ESTAFETAS.append(Estafeta(nome, vehiculo))
            self.clean_estafeta_vars()

    def clean_estafeta_vars(self):
        self.text_estafeta.delete("1.0", "end")
        self.var_vehiculo.set(0)

    def mostar_gerar(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_gerar
        self.clean_gerar_vars()
        self.frame_gerar.pack(pady=50)

    def setup_gerar(self):
        self.frame_gerar = ttk.Frame(self.root)
        self.frame_gerar.pack_forget()

        self.gerar_label = ttk.Label(self.frame_gerar, text="Número de estafetas")
        self.gerar_label.pack(pady=10)

        self.text_n_estafetas = tk.Text(self.frame_gerar, height=1, width=20)
        self.text_n_estafetas.pack(pady=10)

        self.gerar_label = ttk.Label(self.frame_gerar, text="Número de encomendas")
        self.gerar_label.pack(pady=10)

        self.text_n_encomendas = tk.Text(self.frame_gerar, height=1, width=20)
        self.text_n_encomendas.pack(pady=10)

        self.label_gerar_algoritmos = ttk.Label(self.frame_gerar, text="Escolha o algoritmo:")
        self.label_gerar_algoritmos.pack(pady=10)

        self.algoritmo_gerar_var = tk.StringVar()

        self.radio_dfs_gerar = ttk.Radiobutton(
            self.frame_gerar, text="DFS", variable=self.algoritmo_gerar_var, value="dfs")
        self.radio_dfs_gerar.pack()

        self.radio_bfs_gerar = ttk.Radiobutton(
            self.frame_gerar, text="BFS", variable=self.algoritmo_gerar_var, value="bfs")
        self.radio_bfs_gerar.pack()

        self.radio_dijkstra_gerar = ttk.Radiobutton(
            self.frame_gerar, text="Dijkstra", variable=self.algoritmo_gerar_var, value="dijkstra")
        self.radio_dijkstra_gerar.pack()

        self.radio_iddfs_gerar = ttk.Radiobutton(
            self.frame_gerar, text="IDDFS", variable=self.algoritmo_gerar_var, value="iddfs")
        self.radio_iddfs_gerar.pack()

        self.radio_bidirectional_gerar = ttk.Radiobutton(
            self.frame_gerar, text="Bidirectional", variable=self.algoritmo_gerar_var, value="bidirectional")
        self.radio_bidirectional_gerar.pack()

        self.radio_greedy_gerar = ttk.Radiobutton(self.frame_gerar, text="Greedy",
                                            variable=self.algoritmo_gerar_var, value="greedy_search")
        self.radio_greedy_gerar.pack()

        self.radio_astar_gerar = ttk.Radiobutton(self.frame_gerar, text="A*",
                                           variable=self.algoritmo_gerar_var, value="astar_search")
        self.radio_astar_gerar.pack()

        self.btn_executar_gerar = ttk.Button(
            self.frame_gerar, text="Executar", command=self.executar_algoritmo_automatico)
        self.btn_executar_gerar.pack(pady=10)

        self.btn_sair_gerar = ttk.Button(
            self.frame_gerar, text="Sair", command=self.mostrar_menu)
        self.btn_sair_gerar.pack(pady=10)

    def clean_gerar_vars(self):
        self.text_n_estafetas.delete("1.0", "end")
        self.text_n_encomendas.delete("1.0", "end")
        self.algoritmo_gerar_var.set('')

    def mostrar_menu_encomenda(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_encomenda
        self.clean_encomenda_vars()
        self.frame_encomenda.pack(pady=50)


    def setup_menu_encomenda(self):

        self.frame_encomenda = ttk.Frame(self.root)

        ttk.Label(self.frame_encomenda, text="Encomenda:").pack(pady=10)

        self.var_encomenda = tk.StringVar()

        self.text_encomenda1 = tk.Text(self.frame_encomenda, height=1, width=20)
        self.text_encomenda1.pack(pady=10)

        self.enco_label = ttk.Label(self.frame_encomenda, text="Cliente:")
        self.enco_label.pack(pady=10)

        self.text_encomenda2 = tk.Text(self.frame_encomenda, height=1, width=20)
        self.text_encomenda2.pack(pady=10)

        self.enco_label = ttk.Label(self.frame_encomenda, text="Destino:")
        self.enco_label.pack(pady=10)
        
        self.text_encomenda3 = tk.Text(self.frame_encomenda, height=1, width=20)
        self.text_encomenda3.pack(pady=10)

        '''
        self.entry_destino = Entry(self.frame_encomenda, textvariable=self.var_destino_entry)
        self.entry_destino.pack(pady=10)
        '''



        self.enco_label = ttk.Label(self.frame_encomenda, text="Peso:")
        self.enco_label.pack(pady=10)

        self.text_encomenda4 = tk.Text(self.frame_encomenda, height=1, width=20)
        self.text_encomenda4.pack(pady=10)

        ttk.Button(self.frame_encomenda, text="Criar", command=self.save_encomenda).pack()
        ttk.Button(self.frame_encomenda, text="Sair", command=self.mostrar_menu_inicial).pack(pady=10)


    def save_encomenda(self):
        #self.text_encomenda
        Idnt = self.text_encomenda1.get(1.0, "end-1c")
        Client = self.text_encomenda2.get(1.0, "end-2c")
        Origem = self.text_encomenda3.get(1.0, "end-3c")
        Destino = self.text_encomenda4.get(1.0, "end-4c")
        if Client != '' and Origem != '' and Destino != '':
            ENCOMENDAS.append(Encomenda(Idnt, Client, Origem, Destino))
            self.clean_encomenda_vars()
            self.frame_encomenda.pack(pady=50)


    def setup_radio_buttons(self, nodos_destino):
        '''
        self.var_destino = tk.IntVar()

        ttk.Label(self.frame_encomenda, text="Escolha o Nodo de Destino:").pack(pady=10)

        for nodo_id in nodos_destino:
            ttk.Radiobutton(self.frame_encomenda, text=f"Nodo {nodo_id}", variable=self.var_destino, value=nodo_id).pack()

        ttk.Button(self.frame_encomenda, text="Confirmar Destino", command=self.confirmar_destino).pack(pady=10)
        '''


    def confirmar_destino(self):
        nodo_destino = self.var_destino.get()
        # Atualize o objeto Encomenda com o nodo de destino escolhido
        for encomenda in ENCOMENDAS:
            if encomenda.destino == '':
                encomenda.destino = nodo_destino
                break
        self.clean_encomenda_vars()
        self.mostrar_menu_inicial()  # Volte ao menu inicial ou ajuste conforme necessário

    def atualizar_hipoteses_destino(self, *args):
        texto_destino = self.var_destino_entry.get()
        nodos_destino = Encomenda.nodos_por_rua(texto_destino)
        self.setup_radio_buttons(nodos_destino)

    def clean_encomenda_vars(self):
        self.text_encomenda1.delete("1.0", "end")
        self.text_encomenda2.delete("1.0", "end")
        self.text_encomenda3.delete("1.0", "end")
        self.text_encomenda4.delete("1.0", "end")

    def mostrar_menu(self):
        # Esconder a tela de boas-vindas
        self.logo_label.pack_forget()
        self.continuar_btn.pack_forget()
        if self.current_frame != self.root:
            self.current_frame.pack_forget()

        self.current_frame = self.frame_menu_inicial
        # Mostrar o menu de escolha do algoritmo
        self.frame_menu_inicial.pack(pady=50)

    @staticmethod
    def seconds_to_hours_minutes(seconds):
        # Calculate hours and minutes
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # Create a formatted string
        time_str = "{:02}:{:02}".format(int(hours), int(minutes))

        return time_str