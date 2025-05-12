import networkx as nx
import pandas as pd
import os
import matplotlib.pyplot as plt

def mostrar_grafo(G):
    """
    Muestra el grafo con los nodos y las aristas, incluyendo los pesos como etiquetas.
    """
    pos = nx.spring_layout(G)  # Calcula la posición de los nodos
    plt.figure(figsize=(10, 8))
    
    # Dibuja los nodos y las aristas
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    
    # Obtén los pesos de las aristas (atributo 'tiempo')
    edge_labels = nx.get_edge_attributes(G, 'tiempo')  # Cambia 'tiempo' si el atributo tiene otro nombre
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)
    
    # Título del grafo
    plt.title("Grafo de Tráfico con Tiempos de Viaje")
    
    # Crea el directorio output si no existe
    os.makedirs("output", exist_ok=True)
    
    # Guarda el grafo como una imagen
    plt.savefig("output/grafo.png")
    
    # Muestra el grafo en pantalla
    plt.show()

def construir_grafo(path_csv):
    if not os.path.exists(path_csv):
        raise FileNotFoundError(f"El archivo {path_csv} no existe.")
    
    df = pd.read_csv(path_csv)
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(
            row['origen'], row['destino'],
            longitud=row['longitud_km'],
            tiempo=row['tiempo_viaje']
        )
    return G