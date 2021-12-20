from partida import *

# Solicitar nombre del usuario y nivel de dificultad
# Iniciar la partida
partida = Partida(solicitar_datos_jugador(),"Skynet", solicitar_nivel_dificultad())

print(f'Empezamos {partida.jugadorA.nombre} !\nLucharás contra Skynet!!\n\n\n')
temp = input("Pulsar enter para continuar")
clearConsole()

# Exportar las flotas a un archivo JSON para realizar pruebas
exportar_flotas(partida.jugadorA.dict_flota_propia, partida.jugadorB.dict_flota_propia)

#Se alterna la petición de coodenadas para realizar disparos
#El jugador A las introduce por teclado
#El jugador B las genera aleatoriamente
while True:
    temp = ''
    if partida.jugadorA.realizar_disparo(partida.jugadorB.flota_propia, partida.nivel_dificultad) == 'OK':
        if partida.jugadorA.humano:
            temp = input("Has ganado {}!\n\nPulsa ENTER para finalizar.\n".format(partida.jugadorA.nombre))
        else:
            print("Has ganado {}!\n\n".format(partida.jugadorA.nombre))
        break
    else:
        if partida.jugadorA.humano:
            temp = input("Pulsar enter para continuar")
        clearConsole()

    if partida.jugadorB.realizar_disparo(partida.jugadorA.flota_propia, partida.nivel_dificultad) == 'OK':
        if partida.jugadorB.humano:
            temp = input("Has ganado {}!\n\nPulsa ENTER para finalizar.\n".format(partida.jugadorB.nombre))
        else:
            print("Has ganado {}!\n\n".format(partida.jugadorB.nombre))
        break
    else:
        if partida.jugadorB.humano:
            temp = input("Pulsar enter para continuar")
        clearConsole()

# Limpiar la pantalla y generar información sobre la partida
clearConsole()
partida.generar_estadisticas()
sys.exit("\n\nHasta luego {}!!".format(partida.jugadorA.nombre))

