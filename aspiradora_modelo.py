import mesa
import numpy as np
import random
from collections import deque
import time
import heapq

# ------ Nuestro agente sin inteligencia --------
def inicializar_celdas_sucias(ancho, alto, porcentaje_sucio):
    total_celdas = ancho * alto
    num_sucias = int(total_celdas * porcentaje_sucio)
    celdas_sucias = random.sample(range(total_celdas), num_sucias)
    return celdas_sucias

class AspiradoraAgente(mesa.Agent):
    def __init__(self, unique_id, modelo):
        super().__init__(unique_id, modelo)
        self.pos = (1, 1)
        self.movimientos = 0

    def mover(self):
        posibles_pasos = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        nueva_posicion = random.choice(posibles_pasos)
        self.model.grid.move_agent(self, nueva_posicion)

    def aspirar(self):
        if self.pos in self.model.celdas_sucias:
            self.model.celdas_sucias.remove(self.pos)
            print(f"Aspiradora {self.unique_id} ha limpiado la celda {self.pos}.")

    def step(self):
        if self.pos in self.model.celdas_sucias:
            self.aspirar()
        else:
            self.mover()
            self.movimientos += 1


# -------- Nuestro agente con BFS --------
class AspiradoraBFSAgente(AspiradoraAgente):
    def __init__(self, unique_id, modelo):
        super().__init__(unique_id, modelo)
        self.pos = (1, 1)
        self.movimientos = 0
        self.objetivo = None
        self.camino = deque()

    def bfs(self, inicio, objetivo):
        """ Algoritmo BFS para encontrar el camino más corto """
        queue = deque([(inicio, [])])
        visitado = set()

        while queue:
            (actual, camino) = queue.popleft()
            if actual in visitado:
                continue
            visitado.add(actual)
            if actual == objetivo:
                return camino + [actual]

            for vecino in self.model.grid.get_neighborhood(actual, moore=True, include_center=False):
                if vecino not in visitado:
                    queue.append((vecino, camino + [actual]))

    def establecer_objetivo(self):
        """ Encontramos la celda sucia más cercana y establecemos un camino hacia ella """
        if self.model.celdas_sucias:
            distancias = [(celda, self.bfs(self.pos, celda)) for celda in self.model.celdas_sucias]
            distancias_validas = [(celda, camino) for celda, camino in distancias if camino]
            if distancias_validas:
                self.objetivo, self.camino = min(distancias_validas, key=lambda x: len(x[1]))
                self.camino = deque(self.camino)

    def mover(self):
        """ Movemos a nuestro agente segun el camino encontrado por el algoritmo BFS"""
        if not self.camino or self.pos == self.objetivo:
            self.establecer_objetivo()
        if self.camino:
            siguiente_pos = self.camino.popleft()
            self.model.grid.move_agent(self, siguiente_pos)


# -------- Nuestro agente con Dijkstra --------
class AspiradoraDijkstraAgente(AspiradoraAgente):
    def __init__(self, unique_id, modelo):
        super().__init__(unique_id, modelo)
        self.pos = (1, 1)
        self.movimientos = 0
        self.objetivo = None
        self.camino = deque()

    def dijkstra(self, inicio, objetivo):
        """ Algoritmo de Dijkstra para encontrar el camino de costo mínimo """
        queue = [(0, inicio, [])]
        visitado = {inicio: 0} 

        while queue:
            (costo, actual, camino) = heapq.heappop(queue)
            if actual == objetivo:
                return camino + [actual]

            for vecino in self.model.grid.get_neighborhood(actual, moore=True, include_center=False):
                nuevo_costo = costo + 1  # Aquí cada movimiento tiene un costo de 1, puedes modificarlo si es necesario
                if vecino not in visitado or nuevo_costo < visitado[vecino]:
                    visitado[vecino] = nuevo_costo
                    heapq.heappush(queue, (nuevo_costo, vecino, camino + [actual]))

        return None

    def establecer_objetivo(self):
        """ Encontramos la celda sucia más cercana con Dijkstra y establecemos un camino hacia ella """
        if self.model.celdas_sucias:
            distancias = [(celda, self.dijkstra(self.pos, celda)) for celda in self.model.celdas_sucias]
            distancias_validas = [(celda, camino) for celda, camino in distancias if camino]
            if distancias_validas:
                self.objetivo, self.camino = min(distancias_validas, key=lambda x: len(x[1]))
                self.camino = deque(self.camino)

    def mover(self):
        """ Movemos a nuestro agente segun el camino encontrado por el algoritmo Dijkstra """
        if not self.camino or self.pos == self.objetivo:
            self.establecer_objetivo()
        if self.camino:
            siguiente_pos = self.camino.popleft()
            self.model.grid.move_agent(self, siguiente_pos)



class AspiradoraModelo(mesa.Model):
    def __init__(self, num_agentes, ancho, alto, porcentaje_sucio, bfs=False, dijkstra=False):
        super().__init__()
        self.num_agentes = num_agentes
        self.grid = mesa.space.MultiGrid(ancho, alto, True)
        self.schedule = mesa.time.RandomActivation(self)

        celdas_sucias_indices = inicializar_celdas_sucias(ancho, alto, porcentaje_sucio)
        self.celdas_sucias = [(index % ancho, index // ancho) for index in celdas_sucias_indices]

        for i in range(self.num_agentes):
            if bfs:
                agente = AspiradoraBFSAgente(i, self)
            elif dijkstra:
                agente = AspiradoraDijkstraAgente(i, self)
            else:
                agente = AspiradoraAgente(i, self)
            self.schedule.add(agente)
            self.grid.place_agent(agente, (1, 1))
        self.start_time = time.time()

    def step(self):
        self.schedule.step()

    def obtener_resultados(self):
        porcentaje_limpio = (1 - len(self.celdas_sucias) / (self.grid.width * self.grid.height)) * 100
        total_movimientos = sum([agent.movimientos for agent in self.schedule.agents])
        tiempo_ejecucion = time.time() - self.start_time
        return len(self.celdas_sucias) == 0, porcentaje_limpio, total_movimientos, tiempo_ejecucion