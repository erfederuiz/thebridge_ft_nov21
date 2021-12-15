from barco import *
from utils import *
from jugador import *
import types


datos_flota_jugadorA=[[4, 'h', (8,0)],
                     [3, 'v', (1,7)],
                     [3, 'v', (3,4)],
                     [2, 'v', (1,1)],
                     [2, 'v', (6,7)],
                     [2, 'h', (9,7)],
                     [1, 'v', (5,1)],
                     [1, 'v', (1,4)],
                     [1, 'v', (2,9)],
                     [1, 'v', (5,9)]]

datos_flota_jugadorB=[[4, 'h', (1,1)],
                     [3, 'v', (3,1)],
                     [3, 'h', (7,1)],
                     [2, 'v', (1,9)],
                     [2, 'v', (6,8)],
                     [2, 'h', (8,5)],
                     [1, 'v', (4,5)],
                     [1, 'v', (9,0)],
                     [1, 'v', (9,3)],
                     [1, 'v', (9,8)]]

flota_jugadorA=[]
flota_jugadorB=[]

dict_df_jugadorA = {}
dict_df_jugadorB = {}

disparos_jugadorA = {}
disparos_jugadorB = {}

#Generar flota jugador A
for datos_barco in datos_flota_jugadorA:
    comprobar_celdas = Posiciones_barco(datos_barco[0], datos_barco[1], datos_barco[2])
    celdas_barco = comprobar_celdas.calcular_posiciones()
    if celdas_barco != (-1,-1):
        flota_jugadorA.append(Barco(datos_barco[0], datos_barco[1], celdas_barco))
        for tupla in celdas_barco:
            dict_df_jugadorA[traductor_coordenadas_to_df(tupla)] = caracter_barco(datos_barco[1])

#Generar flota jugador B
for datos_barco in datos_flota_jugadorB:
    comprobar_celdas = Posiciones_barco(datos_barco[0], datos_barco[1], datos_barco[2])
    celdas_barco = comprobar_celdas.calcular_posiciones()
    if celdas_barco != (-1,-1):
        flota_jugadorB.append(Barco(datos_barco[0], datos_barco[1], celdas_barco))
        for tupla in celdas_barco:
            dict_df_jugadorB[traductor_coordenadas_to_df(tupla)] = caracter_barco(datos_barco[1])

jugadorA = Jugador(flota_jugadorA,dict_df_jugadorA, disparos_jugadorA)
jugadorB = Jugador(flota_jugadorB,dict_df_jugadorB, disparos_jugadorB)

while True:
    temp = ''
    if jugadorA.realizar_disparo(flota_jugadorB) == 'OK':
        temp = input("Has ganado jugador A!")
        break
    else:
        temp = input("Pulsar enter para continuar")
        clearConsole()

    if jugadorB.realizar_disparo(flota_jugadorA) == 'OK':
        temp = input("Has ganado jugador B!")
        break
    else:
        temp = input("Pulsar enter para continuar")
        clearConsole()




'''
Prueba disparo
if celdas != (-1,-1):
    barco = Barco(4,celdas)
    fronteras = Fronteras_barco(4, 'v', (6,9))
    print(fronteras.calcular())
    for disparo in barco.celdas_barco():
        print(barco.comprobarDisparo(disparo))
else:
    print("Posición erronea")
'''
