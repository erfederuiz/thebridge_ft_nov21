from utils import *

class Jugador:
    def __init__(self,nombre_jugador, flota_propia, dict_flota_propia, dict_disparos):
        self.nombre = nombre_jugador
        self.flota_propia = flota_propia
        self.dict_flota_propia = dict_flota_propia
        self.dict_disparos_jugador = dict_disparos

    def realizar_disparo(self, flota_enemiga):

        for barco in self.flota_propia:
            for celda in barco.celdas.items():
                celda_df = traductor_coordenadas_to_df(celda[0])
                self.dict_flota_propia[celda_df] = celda[1]

        while True:
            clearConsole()
            tablero(self.dict_flota_propia, "\nTu flota {}:\n".format(self.nombre))
            tablero(self.dict_disparos_jugador, "\nTus disparos {}:\n".format(self.nombre))
            coordenada = input("Apunta y dispara!!\n")
            coordenada = traducir_coordenadas_usuario(coordenada)
            for barco_enemigo in flota_enemiga:
                result = barco_enemigo.comprobar_disparo(coordenada)
                if result != agua:
                    self.dict_disparos_jugador[traductor_coordenadas_to_df(coordenada)]=result
                    if self.destruida_flota_enemiga(flota_enemiga):
                        clearConsole()
                        tablero(self.dict_flota_propia, "\nTu flota:\n")
                        tablero(self.dict_disparos_jugador, "\nTus disparos:\n")
                        return 'OK'
                    break

            if result == agua:
                self.dict_disparos_jugador[traductor_coordenadas_to_df(coordenada)] = result
                break

        clearConsole()
        tablero(self.dict_flota_propia, "\nTu flota:\n")
        tablero(self.dict_disparos_jugador, "\nTus disparos:\n")

    def destruida_flota_enemiga(self, flota_enemiga):
        result = True
        for barco in flota_enemiga:
                if barco.estado == 'F':
                    result = False
        return result