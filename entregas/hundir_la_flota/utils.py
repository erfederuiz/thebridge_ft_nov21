import os
import re
import pandas as pd
import numpy as np
import random
import sys
import json
import copy

#Constantes usadas en el programa
#limites del tablero
limit_columnas = 9
limit_filas = 9
#valores de las celdas
agua = 'X'
tocado = 'T'
hundido = 'H'

#Esloras que se van a generar
tipos_barco = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

#Valores numericos correspondientes a caracteres A-J y 1-9
col_strings = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9}
row_strings = {'1':0, '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7, '9':8, '10':9}

#Valor numerico de la columnas de un dataframe y su indice con los valores del tablero de 1 a 9
col_df_to_number = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9}
row_df_to_number = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9}

# de un dataframe y su indice para los valores del tablero de 1 a 9 para fila y columna
col_number_to_df = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J'}
row_number_to_df = {0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8, 8:9, 9:10}

# Funcion para limpiar la pantalla
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def check_coordenadas(tupla):
    '''
    Controla que las coordenadas recibidas en tupla están dentro de los límites del tablero
    :param tupla: (x, y)
    :return:
    '''
    if (tupla[0]>=0 and tupla[0]<=limit_filas) and (tupla[1]>=0 and tupla[1]<=limit_columnas):
        return True
    else:
        return False

def traductor_coordenadas_to_df(tupla):
    '''
    Transforma una tupla en formato (num, num) a una tupla (letter, num)
    :param tupla:
    :return:
    '''
    result = ()
    result = (row_number_to_df[tupla[0]], col_number_to_df[tupla[1]])
    return result

def traductor_dict_to_df(dict_celdas):
    '''
    Transforma las claves de un diccionario en formato (num, num) a una tupla (letter, num)
    :param dict_celdas:
    :return:
    '''
    result = {}
    tuplas_clave = dict_celdas.keys()
    valores_celda = list(dict_celdas.values())
    for i, tupla in enumerate(tuplas_clave):
        nueva_tupla = (row_number_to_df[tupla[0]], col_number_to_df[tupla[1]])
        result[nueva_tupla] = valores_celda[i]
    return result

def pedir_coordenadas(jugador):
    '''
    Solicita unas coordenadas en formato letra número al jugador, p.ej. A1
    No finaliza hasta recibir un input en formato correcto
    :param jugador:
    :return:
    '''
    while True:
        coordenada = input("Apunta y dispara!!\nSi quieres acabar la partida, escribe \"Me piro\":  ")
        if check_input_usuario(coordenada, jugador):
            return coordenada

def traducir_coordenadas_usuario(input_usuario):
    '''
    Transforma una entrada columna fila en formato tablero p.ej. A1 a una tupla (1, 'A')
    :param input_usuario:
    :return:
    '''
    pattern = r'([A-Ja-j])([0-9]+)'
    result = re.search(pattern, input_usuario)
    if result:
        coordenadas = (row_strings[result.group(2)], col_strings[str(result.group(1)).upper()])
        return coordenadas
    else:
        return (-1, -1)


def check_input_usuario(input_usuario, jugador):
    '''
    Comprueba que el jugador ha introducido unas coordenas en formato tablero  A1 - J10
    :param input_usuario:
    :param jugador:
    :return:
    '''
    pattern = r'([A-Ja-j])([0-9]+)'
    if input_usuario.lower() == 'me piro':
        sys.exit("Hasta luego {}!!".format(jugador.nombre))
    result = re.search(pattern, input_usuario)
    return result and int(result.group(2)) <= 10




def tablero(diccionario, mensaje):
    '''
    Recibe un diccionario con items en formato (fila, columna):valor (1,'A'):'X'
    lo carga en un dataframe y lo imprime
    Muestra un mensaje sobre el dataframe
    :param diccionario:
    :param mensaje:
    :return:
    '''
    tab = pd.DataFrame(np.zeros((10, 10)), columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).replace(0, ' ')
    first_element_tup = []
    second_element_tup = []
    valor = [] if bool(diccionario.values()) == False else diccionario.values()
    for key in diccionario:
        first_element_tup.append(key[0])
        second_element_tup.append(key[1])
    for i in range(0, len(valor)):
        if (first_element_tup[i],second_element_tup[i]) in diccionario.keys():
            tab.loc[first_element_tup[i], second_element_tup[i]] = diccionario[first_element_tup[i],second_element_tup[i]]
        else:
             print(" ")

    print(f'{mensaje}')
    print(tab)

def caracter_barco(orientacion):
    '''
    Devuelve el caracter Unicode que se usa para formar barcos dependiendo de la orientación Vertical u Horizontal
    :param orientacion:
    :return:
    '''
    if orientacion == 'h':
        return '\u25B3'
    elif orientacion == 'v':
        return "\u25B7"
    else:
        return ' '



def generar_lista_random(inicio, fin, cantidad):
    '''
    Devuelve una lista con un numero cantidad de enteros, entre inicio y fin
    :param inicio:
    :param fin:
    :param cantidad:
    :return:
    '''
    randomlist = [random.randint(inicio, fin) for _ in range(cantidad)]
    return randomlist

def solicitar_datos_jugador():
    '''
    Solicita el nombre del usuario y controla si quiere acabar la partida
    :return:
    '''
    input_usuario = input("¿Como te llamas?\nSi no quieres seguir pulsa ENTER\n")
    if len(input_usuario)==0:
        sys.exit("Hasta luego !!")
    else:
        return input_usuario


def solicitar_nivel_dificultad():
    '''
    Solicita el nivel de dificultad y controla si el usuario quiere acabar la partida
    :return:
    '''
    print("Introducir el nivel de dificultad (1-5)\nEl nivel marcará el número de disparos por turno que realizará tu oponente\nSi no quieres seguir pulsa ENTER\n")
    while True:
        input_usuario = input()
        if len(input_usuario)==0:
            sys.exit("Hasta luego !!")
        else:
            pattern = r'^([1-5])$'
            result = re.search(pattern, input_usuario)
            if result:
                return int(result.group(1))


def exportar_flotas(dict_flotaA, dict_flotaB):
    '''
    Exporta los diccionarios con las flotas de los usuarios para realizar pruebas
    :param dict_flotaA:
    :param dict_flotaB:
    :return:
    '''
    flotaA = copy.copy(dict_flotaA)
    flotaB = copy.copy(dict_flotaB)
    a_file = open("jugadorA.json", "w")
    b_file = open("jugadorB.json", "w")
    jsonA = transformar_tuplas_dict_disparos(flotaA)
    jsonB = transformar_tuplas_dict_disparos(flotaB)
    json.dump(jsonA, a_file)
    json.dump(jsonB, b_file)
    a_file.close()
    b_file.close()

def transformar_tuplas_dict_disparos(dict_transformar):
    '''
    Transforma un diccionario con keys en formato tupla a otro con keys en formato  string
    :param dict_transformar:
    :return:
    '''
    result = {}
    for key, value in dict_transformar.items():
        result[str(key[0])+key[1]]=value
    return result