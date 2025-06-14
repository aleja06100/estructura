from typing import Any, Optional, List, Tuple

class NodoPila:
    def __init__(self, valor: Any, siguiente: Optional['NodoPila'] = None) -> None:
        self.valor = valor
        self.siguiente = siguiente

class Pila:
    def __init__(self) -> None:
        self.tope: Optional[NodoPila] = None

    def apilar(self, valor: Any) -> None:
        nuevo_nodo = NodoPila(valor, self.tope)
        self.tope = nuevo_nodo

    def desapilar(self) -> Optional[Any]:
        if self.esta_vacia():
            return None
        valor = self.tope.valor
        self.tope = self.tope.siguiente
        return valor

    def esta_vacia(self) -> bool:
        return self.tope is None

class Nodo:
    def __init__(self, posicion: Tuple[int, int], anterior: Optional['Nodo'] = None) -> None:
        self.posicion = posicion
        self.anterior = anterior

class Laberinto:
    def __init__(self, laberinto: List[List[str]]) -> None:
        self.laberinto = laberinto
        self.filas = len(laberinto)
        self.columnas = len(laberinto[0])
        self.inicio = self.encontrar_inicio()
        self.pila = Pila()

    def encontrar_inicio(self) -> Optional[Tuple[int, int]]:
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.laberinto[i][j] == 'S':
                    return (i, j)
        return None

    def es_valido(self, x: int, y: int) -> bool:
        return 0 <= x < self.filas and 0 <= y < self.columnas and self.laberinto[x][y] in ('O', 'E')

    def imprimir_camino(self, nodo: 'Nodo') -> None:
        camino = []
        while nodo:
            camino.append(nodo.posicion)
            nodo = nodo.anterior
        camino.reverse()
        print("Camino recorrido:", camino)

    def resolver(self) -> bool:
        if not self.inicio:
            print("No se encontró el punto de inicio.")
            return False

        self.pila.apilar(Nodo(self.inicio))
        movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while not self.pila.esta_vacia():
            nodo_actual = self.pila.desapilar()
            if nodo_actual is None:
                continue
            x, y = nodo_actual.posicion

            if self.laberinto[x][y] == 'E':
                print("¡Salida encontrada!")
                self.imprimir_camino(nodo_actual)
                return True

            if self.laberinto[x][y] != 'S':  # No marcar la salida ni el inicio
                self.laberinto[x][y] = 'V'

            for dx, dy in movimientos:
                nx, ny = x + dx, y + dy
                if self.es_valido(nx, ny):
                    self.pila.apilar(Nodo((nx, ny), nodo_actual))

        print("No hay salida en el laberinto.")
        return False


# Prueba
laberinto_matriz: List[List[str]] = [
    ['S', 'O', 'X', 'X', 'O'],
    ['X', 'O', 'O', 'X', 'O'],
    ['X', 'X', 'O', 'O', 'X'],
    ['O', 'O', 'X', 'O', 'E'],
    ['X', 'O', 'O', 'O', 'X'],
]

laberinto = Laberinto(laberinto_matriz)
laberinto.resolver()