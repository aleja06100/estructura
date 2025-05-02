import pandas as pd
from typing import Optional


try:
    df = pd.read_csv(
        "./Excel/Directorio_E.S.E._Hospitales_de_Antioquia_con_coordenadas_20250426.csv",
        encoding="utf-8-sig", sep=",", on_bad_lines="skip"
    )
except (FileNotFoundError, pd.errors.ParserError) as e:
    print(f"Error: {e}")
    exit()


df.columns = df.columns.str.strip()
df["Número NIT"] = df["Número NIT"].str.replace(",", "").str.replace('"', "").str.strip()
df = df[df["Número NIT"].str.isnumeric()]
df["Número NIT"] = df["Número NIT"].astype(int

class NodoHospital:
    def __init__(self, nit: int, razon_social: str, sede: str, municipio: str) -> None:
        self.nit: int = nit
        self.razon_social: str = razon_social
        self.sede: str = sede
        self.municipio: str = municipio
        self.izquierda: Optional["NodoHospital"] = None
        self.derecha: Optional["NodoHospital"] = None

class ArbolHospitales:
    def __init__(self) -> None:
        self.raiz: Optional[NodoHospital] = None

    def insertar(
        self, nodo: Optional[NodoHospital], nit: int, razon_social: str, sede: str, municipio: str
    ) -> NodoHospital:
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
            print(f"🔹 NIT: {nodo.nit} | {nodo.razon_social} | {nodo.sede} | {nodo.municipio}")
            self.recorrido_inorder(nodo.derecha)

    def buscar(self, nodo: Optional[NodoHospital], nit_buscado: int) -> str:
        if nodo is None:
            return "Hospital no encontrado"
        if nodo.nit == nit_buscado:
            return f" {nodo.razon_social} | {nodo.sede} | {nodo.municipio}"
        return self.buscar(nodo.izquierda if nit_buscado < nodo.nit else nodo.derecha, nit_buscado)


arbol = ArbolHospitales()
for _, row in df.iterrows():
    arbol.raiz = arbol.insertar(
        arbol.raiz, row["Número NIT"], row["Razón Social Organización"], row["Nombre Sede"], row["Nombre Municipio"]
    )


print("\nHospitales ordenados por NIT:")
arbol.recorrido_inorder(arbol.raiz)
print("\nBuscando hospital con NIT 890980643:")
print(arbol.buscar(arbol.raiz, 890980643))
