import pandas as pd
import numpy as np


def tablero(diccionario):
    import pandas as pd
    import numpy as np
    tab = pd.DataFrame(np.zeros((10, 10)), columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).replace(0, '')
    first_element_tup = []
    second_element_tup = []
    valor = diccionario.values()
    for key in diccionario:
        first_element_tup.append(key[0])
        second_element_tup.append(key[1])
    for i in range(0, len(valor)):
        if (first_element_tup[i],second_element_tup[i]) in diccionario.keys():
            tab.loc[first_element_tup[i], second_element_tup[i]] = diccionario[first_element_tup[i],second_element_tup[i]]
        else:
             print(" ")
    print(tab)


tablero(diccionario = {(6,"A"): "X", (7,"A"): "T", (8,"A"): "T", (9,"A"): "T", (10,"A"): "H"})
tablero(diccionario = {(5,"H"): "X", (4,"H"): "X", (3,"H"): "T", (2,"H"): "T", (1,"H"): "H"})
