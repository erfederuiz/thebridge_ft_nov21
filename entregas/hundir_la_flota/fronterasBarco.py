limit_columnas = 9
limit_filas = 9
inicio_barco=(9,9)
eslora=1
orientacion='h'
celdas = []
next_celda=()

def check_coordenadas(tupla):
    if (tupla[0]>=0 and tupla[0]<=limit_filas) and (tupla[1]>=0 and tupla[1]<=limit_columnas):
        return True
    else:
        return False

next_celda = (inicio_barco[0]-1, inicio_barco[1])
if check_coordenadas(next_celda):
    celdas.append(next_celda)


derecha=0
abajo=0
izquierda=0
arriba=0

derecha=eslora+1 if orientacion=='h' else 2
abajo=3 if orientacion=='h' else eslora+2
izquierda=eslora+2 if orientacion=='h' else 3
arriba=3 if orientacion=='h' else eslora+2

celda_inicial = next_celda
for i in range(1, derecha):
    next_celda=(celda_inicial[0], celda_inicial[1]+i)
    if check_coordenadas(next_celda):
        celdas.append(next_celda)

celda_inicial = next_celda
for i in range(1, abajo):
    next_celda=(celda_inicial[0]+i, celda_inicial[1])
    if check_coordenadas(next_celda):
        celdas.append(next_celda)

celda_inicial = next_celda
for i in range(1, izquierda):
    next_celda=(celda_inicial[0], celda_inicial[1]-i)
    if check_coordenadas(next_celda):
        celdas.append(next_celda)

celda_inicial = next_celda
for i in range(1, arriba):
    next_celda=(next_celda[0]-1, next_celda[1])
    if check_coordenadas(next_celda):
        celdas.append(next_celda)

print(celdas)