import sys
from PyQt5.QtWidgets import QApplication
from front_end_inicio import VentanaInicio
from front_end_juego import VentanaJuego
from tienda import Tienda
from back_end import DCCampo

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication(sys.argv)

    dccampo = DCCampo()
    ventana_inicio = VentanaInicio()
    ventana_juego = VentanaJuego()
    tienda = Tienda()

    dccampo.signal_set(ventana_inicio, ventana_juego, tienda)
    ventana_inicio.signal_set(dccampo, ventana_juego)
    ventana_juego.signal_set(dccampo, tienda)
    tienda.signal_set(dccampo, ventana_juego)

    ventana_inicio.show()

    print('Juego iniciado...')
    sys.exit(app.exec_())
