from utils import *
from barco import *
from jugador import *

class Partida:
    def __init__(self, nombre_jugadorA, nombre_jugadorB):
        self.jugadorA = Jugador(nombre_jugadorA, True, [], {}, {})
        self.jugadorB = Jugador(nombre_jugadorB, False, [], {}, {})

        datos_barcos_A = self.generar_datos_barcos(tipos_barco)
        datos_barcos_B = self.generar_datos_barcos(tipos_barco)

        datos_flota_A = self.generar_flota_jugador(datos_barcos_A)
        datos_flota_B = self.generar_flota_jugador(datos_barcos_B)

        self.jugadorA.flota_propia = datos_flota_A[0]
        self.jugadorA.dict_flota_propia = datos_flota_A[1]

        self.jugadorB.flota_propia = datos_flota_B[0]
        self.jugadorB.dict_flota_propia = datos_flota_B[1]

    def generar_datos_barcos(self, tipos_barco):
        dict_control = {4: 0, 3: 0, 2: 0, 1: 0}
        celdas_ocupadas_barcos = []
        celdas_ocupadas_fronteras = set()
        result = []

        while sum(dict_control.values()) < 10:
            for tipo_barco in tipos_barco:
                while True:
                    # Generar array filas
                    filas = generar_lista_random(0, 9, 1)
                    # Generar array columnas
                    columnas = generar_lista_random(0, 9, 1)
                    # Generar array orientaciones
                    orientacion = list(map(lambda x: 'h' if x == 0 else 'v', generar_lista_random(0, 1, 1)))

                    datos_barco = [tipo_barco, orientacion[0], (filas[0], columnas[0])]
                    comprobar_barco = Posiciones_barco(datos_barco[0], datos_barco[1], datos_barco[2])
                    celdas_barco = comprobar_barco.calcular_posiciones()
                    if celdas_barco != (-1, -1):
                        comprobar_fronteras = Fronteras_barco(datos_barco[0], datos_barco[1], datos_barco[2])
                        celdas_frontera=comprobar_fronteras.calcular()
                        celdas_conflicto_barcos = list(filter(lambda x: x in celdas_ocupadas_barcos, celdas_barco))
                        celdas_conflicto_fronteras = list(filter(lambda x: x in celdas_ocupadas_fronteras, celdas_barco))
                        if len(celdas_conflicto_barcos)==0 and len(celdas_conflicto_fronteras)==0:
                            celdas_ocupadas_barcos += celdas_barco
                            lista_fronteras_intermedia = list(celdas_ocupadas_fronteras) + celdas_frontera
                            celdas_ocupadas_fronteras = set(lista_fronteras_intermedia)
                            dict_control[datos_barco[0]] += 1
                            result.append(datos_barco)
                            break
        return result

    def generar_flota_jugador(self, datos):
        result = []
        array_flota = []
        dict_flota = {}
        for datos_barco in datos:
            comprobar_celdas = Posiciones_barco(datos_barco[0], datos_barco[1], datos_barco[2])
            celdas_barco = comprobar_celdas.calcular_posiciones()
            if celdas_barco != (-1, -1):
                array_flota.append(Barco(datos_barco[0], datos_barco[1], celdas_barco))
                for tupla in celdas_barco:
                    dict_flota[traductor_coordenadas_to_df(tupla)] = caracter_barco(datos_barco[1])
        result.append(array_flota)
        result.append(dict_flota)
        return result


    def generar_estadisticas(self):
        disparosA = self.jugadorA.dict_disparos_jugador
        disparosB = self.jugadorB.dict_disparos_jugador
        infoA = []
        infoB = []

        maximo_jugadas = len(disparosA.items()) if len(disparosA.items()) >= len(disparosB.items()) else len(disparosB.items())

        infoA = [f'{keys[1]}{keys[0]}={value}' for keys, value in disparosA.items()]
        infoB = [f'{keys[1]}{keys[0]}={value}' for keys, value in disparosB.items()]
        linea_datos = ''

        linea_datos += f'Jugadas\t\t\t\tJugadas\n'
        linea_datos += f'{self.jugadorA.nombre}\t\t\t\t{self.jugadorB.nombre}\n'
        linea_datos += f'                      \n'
        for i in range(maximo_jugadas):
            datosA = "    "
            datosB = "    "
            if i < len(disparosA.items()):
                datosA = f'{infoA[i]}'
            if i < len(disparosB.items()):
                datosB = f'{infoB[i]}'

            linea_datos += f'{datosA}\t\t\t\t{datosB}\n'

        print(linea_datos)

        self.resumen_jugadas(self.jugadorA.nombre, self.jugadorA.dict_disparos_jugador)
        self.resumen_jugadas(self.jugadorB.nombre, self.jugadorB.dict_disparos_jugador)




    def resumen_jugadas(self, nombre_jugador, disparos_jugador ):
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




