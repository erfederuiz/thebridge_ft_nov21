from utils import *

class Fronteras_barco:
    def __init__(self, eslora, orientacion, coordenadas):
        self.eslora = eslora
        self.orientacion = orientacion
        self.inicio = coordenadas
        self.celdas = []

    def celdas_contar(self, direccion):
        if direccion == 'derecha':
            return self.eslora + 1 if self.orientacion == 'h' else 2
        elif direccion == 'abajo':
            return 3 if self.orientacion == 'h' else self.eslora + 2
        elif direccion == 'izquierda':
            return self.eslora + 2 if self.orientacion == 'h' else 3
        elif direccion == "arriba":
            return 3 if self.orientacion == 'h' else self.eslora + 2
        else:
            return 0

    def frontera_superior(self):
        celda_inicial = self.celdas[-1]
        for i in range(1, self.celdas_contar("derecha")):
            next_celda = (celda_inicial[0], celda_inicial[1] + i)
            self.celdas.append(next_celda)

    def frontera_derecha(self):
        celda_inicial = self.celdas[-1]
        for i in range(1, self.celdas_contar("abajo")):
            next_celda = (celda_inicial[0] + i, celda_inicial[1])
            self.celdas.append(next_celda)

    def frontera_inferior(self):
        celda_inicial = self.celdas[-1]
        for i in range(1, self.celdas_contar("izquierda")):
            next_celda = (celda_inicial[0], celda_inicial[1] - i)
            self.celdas.append(next_celda)

    def frontera_izquierda(self):
        celda_inicial = self.celdas[-1]
        for i in range(1, self.celdas_contar("arriba")):
            next_celda = (celda_inicial[0] - i, celda_inicial[1])
            self.celdas.append(next_celda)

    def calcular(self):
        next_celda = (self.inicio[0] - 1, self.inicio[1])
        self.celdas.append(next_celda)
        self.frontera_superior()
        self.frontera_derecha()
        self.frontera_inferior()
        self.frontera_izquierda()

        return list(filter(check_coordenadas, self.celdas))
