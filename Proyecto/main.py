
import networkx as nx
import pandas as pd
import os
import matplotlib.pyplot as plt

def mostrar_grafo(G):
    """
    Muestra el grafo con los nodos y las aristas, incluyendo los pesos como etiquetas.
    """
    pos = nx.spring_layout(G) 
    plt.figure(figsize=(10, 8))
    
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    
 
    edge_labels = nx.get_edge_attributes(G, 'tiempo') 
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)
    
 
    plt.title("Grafo de Tráfico con Tiempos de Viaje")
  
    os.makedirs("output", exist_ok=True)
    
 
    plt.savefig("output/grafo.png")
    
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



import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

def entrenar_o_cargar_modelo(path_csv, model_path="models/modelo_tiempo.pkl"):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    if os.path.exists(model_path):
        return joblib.load(model_path)
    
    df = pd.read_csv(path_csv)
    X = df[['dia', 'hora']]
    y = df['tiempo_viaje']
    X_train, _, y_train, _ = train_test_split(X, y, random_state=42)
    modelo = RandomForestRegressor(n_estimators=100)
    modelo.fit(X_train, y_train)
    joblib.dump(modelo, model_path)
    return modelo

def predecir_tiempos(G, modelo, dia_actual, hora_actual):
    for u, v, data in G.edges(data=True):
        X_pred = pd.DataFrame([[dia_actual, hora_actual]], columns=['dia', 'hora'])
        tiempo_estimado = modelo.predict(X_pred)[0]
        data['peso'] = tiempo_estimado



import networkx as nx

def encontrar_ruta_optima(G, source, target):
    try:
        return nx.shortest_path(G, source=source, target=target, weight='peso')
    except nx.NetworkXNoPath:
        raise ValueError(f"No hay ruta entre {source} y {target}.")



import folium
import os

coords = {
    'A': [19.43, -99.13],
    'B': [19.44, -99.12],
    'C': [19.45, -99.13],
    'D': [19.46, -99.14],
    'E': [19.47, -99.13],
    'F': [19.48, -99.12],
}

def mostrar_ruta_en_mapa(ruta, output_path="output/ruta_recomendada.html"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    m = folium.Map(location=[19.44, -99.13], zoom_start=13)
    for i in range(len(ruta) - 1):
        p1, p2 = ruta[i], ruta[i+1]
        folium.PolyLine(
            locations=[coords[p1], coords[p2]],
            color='blue',
            weight=5,
            opacity=0.8
        ).add_to(m)
    m.save(output_path)



import sys
import os
import matplotlib.pyplot as plt
import networkx as nx
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.grafo import construir_grafo, mostrar_grafo


data_path = "data/datos_trafico.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError(f"El archivo {data_path} no existe. Por favor, verifica la ruta.")


G = construir_grafo(data_path)


mostrar_grafo(G)


print(G.edges(data=True))












