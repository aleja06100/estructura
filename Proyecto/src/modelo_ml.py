import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

def entrenar_o_cargar_modelo(path_csv, model_path="models/modelo_tiempo.pkl"):
    # Crea el directorio models si no existe
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Si el modelo ya existe, cárgalo
    if os.path.exists(model_path):
        return joblib.load(model_path)
    
    # Carga los datos y entrena el modelo
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
        # Predice el tiempo de viaje para cada arista
        X_pred = pd.DataFrame([[dia_actual, hora_actual]], columns=['dia', 'hora'])
        tiempo_estimado = modelo.predict(X_pred)[0]
        data['peso'] = tiempo_estimado