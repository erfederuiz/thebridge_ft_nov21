from partida import *

partida = Partida(solicitar_datos_jugador(),"Skynet")

print(f'Empezamos {partida.jugadorA.nombre} !\nLucharás contra Skynet!!\n\n\n')
temp = input("Pulsar enter para continuar")
clearConsole()


while True:
    temp = ''
    if partida.jugadorA.realizar_disparo(partida.jugadorB.flota_propia) == 'OK':
        if partida.jugadorA.humano:
            temp = input("Has ganado {}!\n\n".format(partida.jugadorA.nombre))
        else:
            print("Has ganado {}!\n\n".format(partida.jugadorA.nombre))
        break
    else:
        if partida.jugadorA.humano:
            temp = input("Pulsar enter para continuar")
        clearConsole()

    if partida.jugadorB.realizar_disparo(partida.jugadorA.flota_propia) == 'OK':
        if partida.jugadorB.humano:
            temp = input("Has ganado {}!\n\n".format(partida.jugadorB.nombre))
        else:
            print("Has ganado {}!\n\n".format(partida.jugadorB.nombre))
        break
    else:
        if partida.jugadorB.humano:
            temp = input("Pulsar enter para continuar")
        clearConsole()



