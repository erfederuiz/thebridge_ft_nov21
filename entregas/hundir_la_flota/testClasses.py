from partida import *

partida = Partida("Humano","Skynet")

while True:
    temp = ''
    if partida.jugadorA.realizar_disparo(partida.jugadorB.flota_propia) == 'OK':
        temp = input("Has ganado jugador A!")
        break
    else:
        temp = input("Pulsar enter para continuar")
        clearConsole()

    if partida.jugadorB.realizar_disparo(partida.jugadorA.flota_propia) == 'OK':
        temp = input("Has ganado jugador B!")
        break
    else:
        temp = input("Pulsar enter para continuar")
        clearConsole()



