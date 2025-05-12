import folium
import os

# Coordenadas simuladas para los nodos
coords = {
    'A': [19.43, -99.13],
    'B': [19.44, -99.12],
    'C': [19.45, -99.13],
    'D': [19.46, -99.14],
    'E': [19.47, -99.13],
    'F': [19.48, -99.12],
}

def mostrar_ruta_en_mapa(ruta, output_path="output/ruta_recomendada.html"):
    """
    Genera un mapa interactivo con la ruta óptima y lo guarda como un archivo HTML.
    """
    # Crea el directorio output si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Crea el mapa centrado en una ubicación inicial
    m = folium.Map(location=[19.44, -99.13], zoom_start=13)
    
    # Dibuja la ruta en el mapa
    for i in range(len(ruta) - 1):
        p1, p2 = ruta[i], ruta[i+1]
        folium.PolyLine(
            locations=[coords[p1], coords[p2]],
            color='blue',
            weight=5,
            opacity=0.8
        ).add_to(m)
    
    # Guarda el mapa en el archivo especificado
    m.save(output_path)