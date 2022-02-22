from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
                            QLineEdit, QPushButton, QGridLayout, QMessageBox,\
                            QProgressBar)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QMimeData, QPoint
from PyQt5.QtGui import QPixmap, QTransform, QDrag
from parametros_generales import N, paths_mapa, paths_alcachofa, \
    paths_choclo, paths_objetos, paths_personaje, paths_recursos
from parametros_precios import PRECIO_ALACACHOFAS, PRECIO_AZADA, PRECIO_CHOCLOS, \
    PRECIO_HACHA, PRECIO_LEÑA, PRECIO_ORO, PRECIO_SEMILLA_ALCACHOFAS, \
        PRECIO_SEMILLA_CHOCLOS, PRECIO_TICKET
from functools import partial
from entidades import Jugador

class Tienda(QWidget):

    t_back_game = pyqtSignal()
    t_buscar_jugador = pyqtSignal()
    t_update_inv = pyqtSignal(Jugador, int)
    t_obtener_paginas = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.layout_tienda = QHBoxLayout()
        self.init_gui()

    def init_gui(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('DCCampo - TIENDA')

    def signal_set(self, juego, ventana_juego):
        juego.b_open_shop.connect(self.mostrar_tienda)
        juego.b_entregar_jugador.connect(self.return_obtenido)
        juego.b_entregar_paginas.connect(self.return_obtenido)

    def mostrar_tienda(self, jugador):
        self.jugador = jugador
        self.izq = QVBoxLayout()

        self.obj = QHBoxLayout()
        upper_left = QLabel(self)
        pixmap = QPixmap(paths_recursos['oro'])
        pixmap = pixmap.scaled(N, N)
        upper_left.setPixmap(pixmap)
        precio = QLabel(f'$ {PRECIO_ORO}')
        self.b_vender = QPushButton('Vender', self)
        self.b_vender.setFixedSize(self.b_vender.sizeHint())
        self.b_vender.clicked.connect(partial(self.vender, self.jugador, 'oro', PRECIO_ORO))
        self.obj.addWidget(upper_left)
        self.obj.addWidget(precio)
        self.obj.addWidget(self.b_vender)
        self.izq.addLayout(self.obj)
        self.izq.addStretch(1)

        self.obj = QHBoxLayout()
        middle_left = QLabel(self)
        pixmap = QPixmap(paths_recursos['leña'])
        pixmap = pixmap.scaled(N, N)
        middle_left.setPixmap(pixmap)
        precio = QLabel(f'$ {PRECIO_LEÑA}')
        self.b_vender = QPushButton('Vender', self)
        self.b_vender.setFixedSize(self.b_vender.sizeHint())
        self.b_vender.clicked.connect(partial(self.vender, self.jugador, 'leña', PRECIO_LEÑA))
        self.obj.addWidget(middle_left)
        self.obj.addWidget(precio)
        self.obj.addWidget(self.b_vender)
        self.izq.addLayout(self.obj)
        self.izq.addStretch(1)

        self.obj = QHBoxLayout()
        lower_left = QLabel(self)
        pixmap = QPixmap(paths_alcachofa['semilla'])
        pixmap = pixmap.scaled(N, N)
        lower_left.setPixmap(pixmap)
        precio = QLabel(f'$ {PRECIO_SEMILLA_ALCACHOFAS}')
        self.botones = QVBoxLayout()
        self.b_comprar = QPushButton('Comprar', self)
        self.b_comprar.setFixedSize(self.b_comprar.sizeHint())
        self.b_comprar.clicked.connect(partial(self.comprar, self.jugador, 'semilla_a',\
             PRECIO_SEMILLA_ALCACHOFAS))
        self.b_vender = QPushButton('Vender', self)
        self.b_vender.setFixedSize(self.b_vender.sizeHint())
        self.b_vender.clicked.connect(partial(self.vender, self.jugador, 'semilla_a',\
             PRECIO_SEMILLA_ALCACHOFAS))
        self.botones.addWidget(self.b_comprar)
        self.botones.addWidget(self.b_vender)
        self.obj.addWidget(lower_left)
        self.obj.addWidget(precio)
        self.obj.addLayout(self.botones)
        self.izq.addLayout(self.obj)
        self.izq.addStretch(1)

        self.obj = QHBoxLayout()
        lowest_left = QLabel(self)
        pixmap = QPixmap(paths_choclo['semilla'])
        pixmap = pixmap.scaled(N, N)
        lowest_left.setPixmap(pixmap)
        precio = QLabel(f'$ {PRECIO_SEMILLA_CHOCLOS}')
        self.botones = QVBoxLayout()
        self.b_comprar = QPushButton('Comprar', self)
        self.b_comprar.setFixedSize(self.b_comprar.sizeHint())
        self.b_comprar.clicked.connect(partial(self.comprar, self.jugador, 'semilla_c', \
            PRECIO_SEMILLA_CHOCLOS))
        self.b_vender = QPushButton('Vender', self)
        self.b_vender.setFixedSize(self.b_vender.sizeHint())
        self.b_vender.clicked.connect(partial(self.vender, self.jugador, 'semilla_c', \
            PRECIO_SEMILLA_CHOCLOS))
        self.botones.addWidget(self.b_comprar)
        self.botones.addWidget(self.b_vender)
        self.obj.addWidget(lowest_left)
        self.obj.addWidget(precio)
        self.obj.addLayout(self.botones)
        self.izq.addLayout(self.obj)
        self.izq.addStretch(1)

        self.obj = QHBoxLayout()
        self.b_salir = QPushButton('Salir', self)
        self.b_salir.setFixedSize(self.b_salir.sizeHint())
        self.b_salir.clicked.connect(self.salir)
        self.obj.addWidget(self.b_salir)
        self.dinero_actual = QLabel(f'Dinero actual: $ {self.jugador.dinero}')
        self.obj.addWidget(self.dinero_actual)
        self.izq.addLayout(self.obj)

        self.der = QVBoxLayout()

        self.obj = QHBoxLayout()
        upper_right = QLabel(self)
        pixmap = QPixmap(paths_objetos['azada'])
        pixmap = pixmap.scaled(N, N)
        upper_right.setPixmap(pixmap)
        precio = QLabel(f'$ {PRECIO_AZADA}')
        self.botones = QVBoxLayout()
        self.b_comprar = QPushButton('Comprar', self)
        self.b_comprar.setFixedSize(self.b_comprar.sizeHint())
        self.b_comprar.clicked.connect(partial(self.comprar, self.jugador, 'azada', PRECIO_AZADA))
        self.b_vender = QPushButton('Vender', self)
        self.b_vender.setFixedSize(self.b_vender.sizeHint())
        self.b_vender.clicked.connect(partial(self.vender, self.jugador, 'azada', PRECIO_AZADA))
        self.botones.addWidget(self.b_comprar)
        self.botones.addWidget(self.b_vender)
        self.obj.addWidget(upper_right)
        self.obj.addWidget(precio)
        self.obj.addLayout(self.botones)
        self.der.addLayout(self.obj)
        self.der.addStretch(1)

        self.obj = QHBoxLayout()
        middle_right = QLabel(self)
        pixmap = QPixmap(paths_objetos['hacha'])
        pixmap = pixmap.scaled(N, N)
        middle_right.setPixmap(pixmap)
        precio = QLabel(f'$ {PRECIO_HACHA}')
        self.botones = QVBoxLayout()
        self.b_comprar = QPushButton('Comprar', self)
        self.b_comprar.setFixedSize(self.b_comprar.sizeHint())
        self.b_comprar.clicked.connect(partial(self.comprar, self.jugador, 'hacha', PRECIO_HACHA))
        self.b_vender = QPushButton('Vender', self)
        self.b_vender.setFixedSize(self.b_vender.sizeHint())
        self.b_vender.clicked.connect(partial(self.vender, self.jugador, 'hacha', PRECIO_HACHA))
        self.botones.addWidget(self.b_comprar)
        self.botones.addWidget(self.b_vender)
        self.obj.addWidget(middle_right)
        self.obj.addWidget(precio)
        self.obj.addLayout(self.botones)
        self.der.addLayout(self.obj)
        self.der.addStretch(1)

        self.obj = QHBoxLayout()
        lower_right = QLabel(self)
        pixmap = QPixmap(paths_alcachofa['icono'])
        pixmap = pixmap.scaled(N, N)
        lower_right.setPixmap(pixmap)
        precio = QLabel(f'$ {PRECIO_ALACACHOFAS}')
        self.b_vender = QPushButton('Vender', self)
        self.b_vender.setFixedSize(self.b_vender.sizeHint())
        self.b_vender.clicked.connect(partial(self.vender, self.jugador, 'alcachofa', \
            PRECIO_ALACACHOFAS))
        self.obj.addWidget(lower_right)
        self.obj.addWidget(precio)
        self.obj.addWidget(self.b_vender)
        self.der.addLayout(self.obj)
        self.der.addStretch(1)

        self.obj = QHBoxLayout()
        lowest_right = QLabel(self)
        pixmap = QPixmap(paths_choclo['icono'])
        pixmap = pixmap.scaled(N, N)
        lowest_right.setPixmap(pixmap)
        precio = QLabel(f'$ {PRECIO_CHOCLOS}')
        self.b_vender = QPushButton('Vender', self)
        self.b_vender.setFixedSize(self.b_vender.sizeHint())
        self.b_vender.clicked.connect(partial(self.vender, self.jugador, 'choclo', \
            PRECIO_CHOCLOS))
        self.obj.addWidget(lowest_right)
        self.obj.addWidget(precio)
        self.obj.addWidget(self.b_vender)
        self.der.addLayout(self.obj)
        self.der.addStretch(1)

        self.obj = QHBoxLayout()
        ticket = QLabel(self)
        pixmap = QPixmap(paths_objetos['ticket'])
        pixmap = pixmap.scaled(N, N)
        ticket.setPixmap(pixmap)
        precio = QLabel(f'$ {PRECIO_TICKET}')
        self.b_comprar = QPushButton('Comprar', self)
        self.b_comprar.setFixedSize(self.b_comprar.sizeHint())
        self.b_comprar.clicked.connect(partial(self.comprar, self.jugador, 'ticket', \
            PRECIO_TICKET))
        self.obj.addWidget(ticket)
        self.obj.addWidget(precio)
        self.obj.addWidget(self.b_comprar)
        self.der.addLayout(self.obj)

        self.layout_tienda.addLayout(self.izq)
        self.layout_tienda.addLayout(self.der)
        self.setLayout(self.layout_tienda)
        self.show()

    def comprar(self, jugador, objeto, precio):
        if jugador.dinero >= int(precio):
            if objeto == 'semilla_a':
                jugador.inventario_semillas['semilla_a'] += 1
            elif objeto == 'semilla_c':
                jugador.inventario_semillas['semilla_c'] += 1
            else:
                jugador.inventario[objeto] += 1
            jugador.dinero -= int(precio)
            self.dinero_actual = QLabel(f'Dinero actual: $ {self.jugador.dinero}')
            self.clear_layout(self.layout_tienda)
            self.mostrar_tienda(jugador)
            [pag_actual, _] = self.obtener_paginas()
            self.t_update_inv.emit(jugador, pag_actual)
        else:
            self.message_box('No posee suficiente dinero para comprar el artículo')

    def vender(self, jugador, objeto, precio):
        if jugador.inventario[objeto] > 0:
            if objeto == 'semilla_a':
                jugador.inventario_semillas['semilla_a'] -= 1
            elif objeto == 'semilla_c':
                jugador.inventario_semillas['semilla_c'] -= 1
            else:
                jugador.inventario[objeto] -= 1
            jugador.dinero += int(precio)
            self.dinero_actual = QLabel(f'Dinero actual: $ {self.jugador.dinero}')
            self.clear_layout(self.layout_tienda)
            self.mostrar_tienda(jugador)
            [pag_actual, _] = self.obtener_paginas()
            self.t_update_inv.emit(jugador, pag_actual)
        else:
            self.message_box('No posee el artículo que desea vender')

    def salir(self):
        jugador = self.obtener_jugador()
        jugador.shop = False
        self.t_back_game.emit()
        self.clear_layout(self.layout_tienda)
        self.hide()

    def return_obtenido(self, signal):
        self.obtenido = signal

    def obtener_jugador(self):
        self.t_buscar_jugador.emit()
        return self.obtenido

    def obtener_paginas(self):
        self.t_obtener_paginas.emit()
        return self.obtenido

    def message_box(self, text):
        mensaje = QMessageBox(self)
        mensaje.setText(text)
        mensaje.setWindowTitle('Error')
        mensaje.addButton(QMessageBox.Ok)
        mensaje.show()

    def clear_layout(self, layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())
