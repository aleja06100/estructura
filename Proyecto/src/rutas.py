import networkx as nx

def encontrar_ruta_optima(G, source, target):
    """
    Encuentra la ruta más corta entre dos nodos en un grafo dirigido,
    utilizando el peso de las aristas como criterio.
    """
    try:
        return nx.shortest_path(G, source=source, target=target, weight='peso')
    except nx.NetworkXNoPath:
        raise ValueError(f"No hay ruta entre {source} y {target}.")