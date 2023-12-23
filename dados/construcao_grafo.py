import networkx as nx
import osmnx as ox


def construir_grafo():
    # Constrói grafo usando o OpenStreetMap (OSM)
    g = ox.graph_from_place('Braga, Braga', network_type="drive")

    # Calcula distâncias entre nodos e adiciona-as às arestas
    ox.distance.add_edge_lengths(g)

    # Remove ruas (arestas) sem nome do grafo
    edges = ox.graph_to_gdfs(g, nodes=False, edges=True)
    edges_filtered = edges[~edges['name'].apply(
        lambda x: isinstance(x, float))]
    edges_to_remove = set(g.edges) - set(edges_filtered.index)
    g.remove_edges_from(edges_to_remove)

    # Passo anterior resulta em vários nodos e arestas isolados
    # Aqui pegamos na maior componente ligada do grafo, removendo as componentes isoladas (nodos e arestas)
    g_un = g.to_undirected()
    largest_component = max(nx.connected_components(g_un), key=len)
    g_un = g_un.subgraph(largest_component)

    # Mudar o nome (identificação) dos nodos para conveniência de utilização apenas
    # Inicialmente vêm com um número grande (osmid) como identificador. Aqui são numerados por ordem crescente
    nodes, edges = ox.graph_to_gdfs(g_un)
    node_rename_mapping = {old_node: str(
        new_node) for new_node, old_node in enumerate(g_un.nodes, start=0)}
    g_un = nx.relabel_nodes(g_un, node_rename_mapping)

    # Remoção de atributos dados pelo OSM que não são importantes
    # Adicção de atributos extra
    g_un_g = nx.MultiGraph(g_un)
    for u, v, data in g_un_g.edges(data=True):
        data['traffic'] = 1
        data['blocked'] = False
        data.pop('osmid', None)
        data.pop('oneway', None)
        data.pop('ref', None)
        data.pop('geometry', None)
        data.pop('maxspeed', None)
        data.pop('bridge', None)
        data.pop('lanes', None)
        data.pop('highway', None)
        data.pop('reversed', None)
        data.pop('junction', None)
        data.pop('access', None)
        data.pop('tunnel', None)
        data.pop('width', None)
    for node, data in g_un_g.nodes(data=True):
        # data.pop('x', None)
        # data.pop('y', None)
        data.pop('ref', None)
        data.pop('geometry', None)
        data.pop('highway', None)
        data.pop('street_count', None)

    # Representação gráfico do grafo
    # fig, ax = ox.plot_graph(g_un, figsize=(25, 25))
    # fig.savefig("grafo.png", bbox_inches='tight')

    # Guarda o grafo em formato gml num ficheiro
    nx.write_gml(g_un_g, './dados/grafo.gml')
