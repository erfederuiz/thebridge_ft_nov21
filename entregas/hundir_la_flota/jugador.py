from utils import *

class Jugador:
    def __init__(self,nombre_jugador, es_humano, flota_propia, dict_flota_propia, dict_disparos):
        self.nombre = nombre_jugador
        self.humano = es_humano
        self.flota_propia = flota_propia
        self.dict_flota_propia = dict_flota_propia
        self.dict_disparos_jugador = dict_disparos

    def realizar_disparo(self, flota_enemiga, nivel_dificultad):
        '''
        El jugador realiza un disparo sobre la flota enemiga
        El jugador A (humano) introduce el disparo por teclado
        El jugador B (programa) genera las coordenadas de forma aleatoria
        nivel_dificultad indica los disparos que el jugador B realizará en cada turno

        Despues de cada disparo se comprueba si la flota enemiga sigue con algún barco a flote
        :param flota_enemiga:
        :param nivel_dificultad:
        :return:
        '''
        num_disparos = 0
        # Pasamos los datos de la flota en formato (fila,columna) a formato dicccionario traducido a dataframe
        for barco in self.flota_propia:
            for celda in barco.celdas.items():
                celda_df = traductor_coordenadas_to_df(celda[0])
                self.dict_flota_propia[celda_df] = celda[1]
        coordenada_previa = (-1, -1)
        resultado_previo = None
        while True:
            #se limpia la pantalla y se solicitan coordenadas
            clearConsole()
            if self.humano:
                tablero(self.dict_flota_propia, "\nTu flota {}:\n".format(self.nombre))
                tablero(self.dict_disparos_jugador, "\nTus disparos {}:\n".format(self.nombre))
                coordenada = pedir_coordenadas(self)
                coordenada = traducir_coordenadas_usuario(coordenada)
            else:
                coordenada = self.generar_disparo(coordenada_previa, resultado_previo)
                coordenada_previa = coordenada

            #Se comprueba si la coordenada introducida pertenece a barco de la flota enemiga
            for barco_enemigo in flota_enemiga:
                resultado = barco_enemigo.comprobar_disparo(coordenada)
                if resultado != agua:
                    resultado_previo = resultado
                    self.dict_disparos_jugador[traductor_coordenadas_to_df(coordenada)] = resultado

                    # Comprobar si se ha eliminado la flota enemiga
                    if self.destruida_flota_enemiga(flota_enemiga):
                        if self.humano:
                            clearConsole()
                            tablero(self.dict_flota_propia, "\nTu flota {}:\n".format(self.nombre))
                            tablero(self.dict_disparos_jugador, "\nTus disparos {}:\n".format(self.nombre))
                        return 'OK'
                    break
            #Controlar salida del while ante un disparo erróneo
            #Para el jugador A, sale despues de un fallo
            # Para el jugador B controla el número de fallos en función de nivel de dificultad
            num_disparos += 1
            if resultado == agua:
                self.dict_disparos_jugador[traductor_coordenadas_to_df(coordenada)] = resultado
                if self.humano:
                    break
                else:
                    if num_disparos >= nivel_dificultad:
                        break

        if self.humano:
            clearConsole()
            tablero(self.dict_flota_propia, "\nTu flota {}:\n".format(self.nombre))
            tablero(self.dict_disparos_jugador, "\nTus disparos {}:\n".format(self.nombre))


    def destruida_flota_enemiga(self, flota_enemiga):
        '''
        Comprueba que quede algún barco en estado F (a flote)
        :param flota_enemiga:
        :return:
        '''
        result = True
        for barco in flota_enemiga:
                if barco.estado == 'F':
                    result = False
        return result

    def generar_disparo(self, coordenada_previa, resultado_previo):
        '''
        Generar una coordenada aleatoria en formato (fila,columna)
        se comprueba que el jugador no ha realizado previamente ese disparo
        :param coordenada_previa:
        :param resultado_previo:
        :return:
        '''
        coordenada_df = (-1, -1)
        while True:
            # Generar array filas
            filas = generar_lista_random(0, 9, 1)
            # Generar array columnas
            columnas = generar_lista_random(0, 9, 1)
            coordenada = (filas[0], columnas[0])
            coordenada_df = traductor_coordenadas_to_df(coordenada)

            if len(self.dict_disparos_jugador.keys() ) == 0:
                break
            if coordenada_df not in self.dict_disparos_jugador.keys():
                break

        return coordenada