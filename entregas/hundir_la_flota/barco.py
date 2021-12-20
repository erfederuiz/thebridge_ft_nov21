from utils import *

class Barco():
    '''
    Almacena los datos de un barco de la flota
    '''
    def __init__(self, eslora, orientacion, celdas):
        self.eslora = eslora
        self.celdas = {}
        self.estado = 'F'
        self.orientacion = orientacion
        for celda in celdas:
            self.celdas[celda] = caracter_barco(orientacion)

    def celdas_barco(self):
        '''
        Devuelve en una lista las celdas que forman un barco
        :return:
        '''
        return self.celdas.keys()

    def comprobar_disparo(self, disparo):
        '''
        Comprueba si un disparo recibido ha acertado y en ese caso devuelve el estado final del barco
        :param disparo:
        :return:
        '''
        if disparo in list(self.celdas.keys()):
            if self.celdas[disparo]==caracter_barco(self.orientacion):
                self.celdas[disparo]=tocado

            valoresAciertos = list(filter(lambda x : x == tocado or x == hundido, self.celdas.values()))

            if len(valoresAciertos) == self.eslora:
                self.celdas[disparo] = hundido
                self.estado='H'
                return hundido
            else:
                self.estado = 'T'
                return tocado
        else:
            return agua


class Posiciones_barco:
    '''
    A partir de una celda y la orientación calcula las posiciones que ocupa un barco
    comprueba que todas las celdas estén dentro de los límites del tablero
    '''
    def __init__(self, eslora, orientacion, coordenadas):
        self.eslora = eslora
        self.orientacion = orientacion
        self.inicio = coordenadas
        self.celdas = []
        self.celdas.append(self.inicio)

    def calcular_posiciones(self):
        for i in range(1, self.eslora):
            last_celda = self.celdas[-1]
            if self.orientacion == 'h':
                proxima_celda = (last_celda[0], last_celda[1] + 1)
                self.celdas.append(proxima_celda if check_coordenadas(proxima_celda) else (-1, -1))
            else:
                proxima_celda = (last_celda[0] + 1, last_celda[1])
                self.celdas.append(proxima_celda if check_coordenadas(proxima_celda) else (-1, -1))

            if self.celdas[-1] == (-1, -1):
                self.celdas = (-1, -1)
                break
        return tuple(self.celdas)

class Fronteras_barco:
    '''
    A partir de una celda, genera las celdas que rodean a un barco y las devuelve en un listado
    controla que las celdas estén dentro de los límites del tablero
    '''
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
