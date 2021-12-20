from utils import *
from barco import *
from jugador import *

class Partida:
    '''

    '''
    def __init__(self, nombre_jugadorA, nombre_jugadorB, nivel_dificultad):
        '''
        Se crea la partida con los dos jugadores y las flotas y control de disparos inicialmente vacíos
        :param nombre_jugadorA:
        :param nombre_jugadorB:
        :param nivel_dificultad:
        '''
        self.nivel_dificultad = nivel_dificultad
        self.jugadorA = Jugador(nombre_jugadorA, True, [], {}, {})
        self.jugadorB = Jugador(nombre_jugadorB, False, [], {}, {})

        #Genear los datos iniciales de las celdas donde se ubicarán los barcos
        datos_barcos_A = self.generar_datos_barcos(tipos_barco)
        datos_barcos_B = self.generar_datos_barcos(tipos_barco)

        #Generar los datos aleatoria sobre la flota de cada jugador
        datos_flota_A = self.generar_flota_jugador(datos_barcos_A)
        datos_flota_B = self.generar_flota_jugador(datos_barcos_B)

        # Se genera una lista con dos estruturas de datos
        # 0 lista con los datos sobre cada barco
        # 1 Array con los datos de cada barco traducidos a formato dataframe
        self.jugadorA.flota_propia = datos_flota_A[0]
        self.jugadorA.dict_flota_propia = datos_flota_A[1]

        self.jugadorB.flota_propia = datos_flota_B[0]
        self.jugadorB.dict_flota_propia = datos_flota_B[1]

    def generar_datos_barcos(self, tipos_barco):
        '''
        Generar una lista de las características iniciales de los barcos de la flota
        para cada barco: eslora, orientacion, celda-inicial
        :param tipos_barco:
        :return:
        '''
        dict_control = {4: 0, 3: 0, 2: 0, 1: 0}
        celdas_ocupadas_barcos = []
        celdas_ocupadas_fronteras = set()
        result = []
        # Hasta que no se hayan generado diez barcos no finaliza el bucle
        # se controla en los valores de dict_control  key eslora : value numero de barcos de esa eslora
        while sum(dict_control.values()) < 10:
            for tipo_barco in tipos_barco:
                while True:
                    # Para cada eslora de barco generamos una (fila, columna) y orientación vertical/horizontal
                    # Generar array filas
                    filas = generar_lista_random(0, 9, 1)
                    # Generar array columnas
                    columnas = generar_lista_random(0, 9, 1)
                    # Generar array orientaciones
                    orientacion = list(map(lambda x: 'h' if x == 0 else 'v', generar_lista_random(0, 1, 1)))

                    #Comprobamos si las celdas generadas están dentro de los límites del tablero
                    datos_barco = [tipo_barco, orientacion[0], (filas[0], columnas[0])]
                    comprobar_barco = Posiciones_barco(datos_barco[0], datos_barco[1], datos_barco[2])
                    celdas_barco = comprobar_barco.calcular_posiciones()
                    if celdas_barco != (-1, -1):
                        #Generamos las celdas que hay alrededor del barco
                        comprobar_fronteras = Fronteras_barco(datos_barco[0], datos_barco[1], datos_barco[2])
                        celdas_frontera=comprobar_fronteras.calcular()
                        celdas_conflicto_barcos = list(filter(lambda x: x in celdas_ocupadas_barcos, celdas_barco))
                        celdas_conflicto_fronteras = list(filter(lambda x: x in celdas_ocupadas_fronteras, celdas_barco))
                        #Si no hay conflicto de las celdas del barco con otros barcos o fronteras de barco
                        #guardamos las celdas en una caché para facilitar las comprobaciones
                        #Tenemos por un lado una caché para celdas de barco y otra para celdas de fronteras
                        if len(celdas_conflicto_barcos)==0 and len(celdas_conflicto_fronteras)==0:
                            celdas_ocupadas_barcos += celdas_barco
                            lista_fronteras_intermedia = list(celdas_ocupadas_fronteras) + celdas_frontera
                            celdas_ocupadas_fronteras = set(lista_fronteras_intermedia)
                            #Anotamos el tipo de barco para el que hemos generado los datos
                            # salimos del ciclo while infinito para generar  datos para un barco
                            dict_control[datos_barco[0]] += 1
                            result.append(datos_barco)
                            break
        return result

    def generar_flota_jugador(self, datos):
        '''
        A partir de una lista de características de los barcos eslora, orientación, celda-inicial
        se genera la flota del jugador
        :param datos:
        :return:
        '''
        result = []
        array_flota = []
        dict_flota = {}
        for datos_barco in datos:
            #Crear un objeto de tipo Posciones_barco para calcular las celdas del barco
            comprobar_celdas = Posiciones_barco(datos_barco[0], datos_barco[1], datos_barco[2])
            celdas_barco = comprobar_celdas.calcular_posiciones()
            if celdas_barco != (-1, -1):
                # Si las información del barco es corrrecta añadirlo a la lista de barcos que representa la flota
                array_flota.append(Barco(datos_barco[0], datos_barco[1], celdas_barco))
                for tupla in celdas_barco:
                    #Generar el diccionario en el formato que permita imprimirlo usando un dataframe
                    dict_flota[traductor_coordenadas_to_df(tupla)] = caracter_barco(datos_barco[1])
        result.append(array_flota)
        result.append(dict_flota)
        return result


    def generar_estadisticas(self):
        '''
        Imprime en pantalla los disparos que ha realizado cada jugador y un resumen de las jugadas realizadas
        :return:
        '''
        disparosA = self.jugadorA.dict_disparos_jugador
        disparosB = self.jugadorB.dict_disparos_jugador
        infoA = []
        infoB = []

        maximo_jugadas = len(disparosA.items()) if len(disparosA.items()) >= len(disparosB.items()) else len(disparosB.items())

        infoA = [f'{keys[1]}{keys[0]}={value}' for keys, value in disparosA.items()]
        infoB = [f'{keys[1]}{keys[0]}={value}' for keys, value in disparosB.items()]

        datos_resumen = []
        datos_resumen.append(['Jugadas '+self.jugadorA.nombre, 'Jugadas '+self.jugadorB.nombre])
        for i in range(maximo_jugadas):
            datosA = "    "
            datosB = "    "
            if i < len(disparosA.items()):
                datosA = f'{infoA[i]}'
            if i < len(disparosB.items()):
                datosB = f'{infoB[i]}'
            datos_resumen.append([datosA, datosB])

        col_width = max(len(word) for row in datos_resumen for word in row) + 2  # padding
        for row in datos_resumen:
            print ("".join(word.ljust(col_width) for word in row))

        self.resumen_jugadas(self.jugadorA.nombre, self.jugadorA.dict_disparos_jugador)
        self.resumen_jugadas(self.jugadorB.nombre, self.jugadorB.dict_disparos_jugador)


    def resumen_jugadas(self, nombre_jugador, disparos_jugador ):
        '''
        Utiliza una serie pandas para realizar un resumen del diccionario donde se han almacenado los disparos del jugador
        y su resultado
        :param nombre_jugador:
        :param disparos_jugador:
        :return:
        '''
        disparos = disparos_jugador
        jugadas = list(disparos.values())
        indx = [*range(1, len(jugadas) + 1, 1)]
        x = pd.Series(jugadas, index=indx)
        total = x.describe()['count']
        tipos_jugada = {'T': 'Tocados', 'H': 'Hundidos', 'X': 'Agua'}
        print(f'\n\nJugadas de {nombre_jugador}')
        print(f'Número de disparos: {x.describe()["count"]}')
        for m in [f'{tipos_jugada[j]}: {x.value_counts()[j]}' for j in list(x.value_counts().keys())]:
            print(m)




