import pandas as pd
from typing import Optional

df = pd.read_csv("./ejerciciosDeExcel/Directorio_E.S.E._Hospitales_de_Antioquia_con_coordenadas_20250426.csv", 
                 encoding='utf-8-sig', sep=',')

print(df.columns)

df.rename(columns={"NÃºmero NIT": "Número NIT"}, inplace=True)

df["Número NIT"] = df["Número NIT"].str.replace(",", "").str.replace('"', "").astype(int)

df.columns = df.columns.str.strip()

class NodoHospital:
    def __init__(self, nit: int, razon_social: str, sede: str, municipio: str):
        self.nit: int = nit
        self.razon_social: str = razon_social
        self.sede: str = sede
        self.municipio: str = municipio
        self.izquierda: Optional[NodoHospital] = None
        self.derecha: Optional[NodoHospital] = None

class ArbolHospitales:
    def __init__(self):
        self.raiz: Optional[NodoHospital] = None

    def insertar(self, nodo: Optional[NodoHospital], nit: int, razon_social: str, sede: str, municipio: str) -> NodoHospital:
        if nodo is None:
            return NodoHospital(nit, razon_social, sede, municipio)
        if nit < nodo.nit:
            nodo.izquierda = self.insertar(nodo.izquierda, nit, razon_social, sede, municipio)
        else:
            nodo.derecha = self.insertar(nodo.derecha, nit, razon_social, sede, municipio)
        return nodo

    def recorrido_inorder(self, nodo: Optional[NodoHospital]) -> None:
        if nodo:
            self.recorrido_inorder(nodo.izquierda)
            print(f"NIT: {nodo.nit} | Organización: {nodo.razon_social} | "
                  f"Sede: {nodo.sede} | Municipio: {nodo.municipio}")
            self.recorrido_inorder(nodo.derecha)

arbol = ArbolHospitales()

for _, row in df.iterrows():
    arbol.raiz = arbol.insertar(
        arbol.raiz,
        row["Número NIT"],  
        row["Razón Social Organización"],  
        row["Nombre Sede"],  
        row["Nombre Municipio"]  
    )

print("\n Hospitales ordenados por NIT:")
arbol.recorrido_inorder(arbol.raiz)

def buscar_hospital(nodo: Optional[NodoHospital], nit_buscado: int) -> str:
    if nodo is None:
        return "Hospital no encontrado"
    if nodo.nit == nit_buscado:
        return f" Organización: {nodo.razon_social}\n   Sede: {nodo.sede}\n   Municipio: {nodo.municipio}"
    elif nit_buscado < nodo.nit:
        return buscar_hospital(nodo.izquierda, nit_buscado)
    else:
        return buscar_hospital(nodo.derecha, nit_buscado)

print("\n  Buscando hospital con NIT 890980643:")
print(buscar_hospital(arbol.raiz, 890980643))

