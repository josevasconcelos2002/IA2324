import networkx as nx
import matplotlib.pyplot as plt


def build_graph():

    nodes_info = {}
    with open("./dados/freguesias.txt", "r") as file:
        i = 1
        for line in file:
            freguesia = line.strip()
            nodes_info.update({str(i): {"nome": freguesia, "ocupado": False}})
            i += 1

    edges = {}
    with open("./dados/arestas.txt", "r") as file:
        for line in file:
            origem, destino, distancia = line.split(";")
            edges.update({(origem, destino): float(distancia)})

    g = nx.Graph()
    g.add_nodes_from(nodes_info.keys())
    g.add_edges_from(edges)

    return g, edges


def draw_graph(g, edges):
    seed_value = 14
    pos = nx.spring_layout(g, seed=seed_value)

    plt.figure(figsize=(14, 11))
    nx.draw(g, pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edges)
    plt.savefig("./dados/grafo.png", format="png")
    plt.show()


def main():
    g, edges = build_graph()
    draw_graph(g, edges)


if __name__ == "__main__":
    main()
