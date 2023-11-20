import networkx as nx
import matplotlib.pyplot as plt
from estafeta import Estafeta
from encomenda import Encomenda
import algoritmos as alg


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


def draw_graph(g, edges):
    seed_value = 14
    pos = nx.spring_layout(g, seed=seed_value)

    plt.figure(figsize=(14, 11))
    nx.draw(g, pos, with_labels=True, font_weight='bold')
    edge_labels = {(edge[0], edge[1]): f"{edge[2]['distance']:.2f}" for edge in edges}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    plt.savefig("./dados/grafon.png", format="png")
    plt.show()


def main():
    g, edges = build_graph()
    # draw_graph(g, edges)

    # mini testes
    est1 = Estafeta(1, 1)
    enc1 = Encomenda(1, "Fabio", "3", "10", 3, 10)
    # print(est1.vehicle.value["speed"])
    visited_dfs, path_dfs, cost_dfs = alg.dfs(g, enc1.origin, enc1.destination)
    print(f"DFS:\nVisited: {visited_dfs}\nPath: {path_dfs}\nCost: {cost_dfs} kms")
    visited_bfs, path_bfs, cost_bfs = alg.bfs(g, enc1.origin, enc1.destination)
    print(f"BFS:\nVisited: {visited_bfs}\nPath: {path_bfs}\nCost: {cost_bfs} kms")
    visited_custo_uniforme, path_custo_uniforme, cost_custo_uniforme = alg.custo_uniforme(g, enc1.origin, enc1.destination)
    print(f"custo_uniforme:\nVisited: {visited_custo_uniforme}\nPath: {path_custo_uniforme}\nCost: {cost_custo_uniforme} kms")


if __name__ == "__main__":
    main()
