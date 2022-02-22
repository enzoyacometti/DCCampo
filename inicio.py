from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
                            QLineEdit, QPushButton, QGridLayout, QMessageBox,\
                            QProgressBar)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QMimeData, QPoint
from PyQt5.QtGui import QPixmap, QTransform, QDrag
from parametros_generales import paths_mapa, N, ENERGIA_JUGADOR, paths_personaje, \
    P_SIZE, t, paths_alcachofa, paths_choclo, paths_recursos, paths_objetos
import itertools

class CargarMapa():
    f_obtener_hora_dia = pyqtSignal()
    f_obtener_dinero = pyqtSignal()
    f_pag_der = pyqtSignal()
    f_pag_izq = pyqtSignal()
    f_pausar_reanudar = pyqtSignal()
    f_salir = pyqtSignal()
    f_obtener_paginas = pyqtSignal()
    f_obtener_jugador = pyqtSignal()

    def __init__(self):
        self.layout_general = QHBoxLayout()
        self.pausado = False
        self.key_pressed = None
        self.setAcceptDrops(True)
        self.obtenido = None
        self.boxes = []

        self.init_gui

    def init_gui(self):
        self.str_cheat = set()
        

    def transformar_posicion_pixel(self, posicion):
        # Solo para objetos no móviles
        posicion = (posicion[0], posicion[1])
        pixel = tuple(map(lambda x: x*N, posicion))[::-1]
        return pixel   

    def return_obtenido(self, signal):
        self.obtenido = signal

    def obtener_hora_dia(self):
        self.f_obtener_hora_dia.emit()
        return self.obtenido

    def obtener_dinero(self):
        self.f_obtener_dinero.emit()
        return self.obtenido

    def obtener_paginas(self):
        self.f_obtener_paginas.emit()
        return self.obtenido

    def obtener_jugador(self):
        self.f_obtener_jugador.emit()
        return self.obtenido

    def pag_derecha(self):
        self.f_pag_der.emit()

    def pag_izquierda(self):
        self.f_pag_izq.emit()

    def pag_derecha_semillas(self):
        pass

    def pag_izquierda_semillas(self):
        pass

    def actualizar(self):
        self.f_send_key.emit(self.key_pressed)

    def actualizar_hora_dinero(self):
        [hora, dia] = self.obtener_hora_dia()
        dinero = self.obtener_dinero()
        jugador = self.obtener_jugador()
        self.dinero.setText(f'Dinero $: {dinero}')
        self.hora.setText(f'Hora: {hora}')
        self.dia.setText(f'Día: {dia}')
        self.energia.setValue(jugador.energia)
        if jugador.energia <= 0:
            self.message_box('loss')

    def actualizar_inventario(self):
        jugador = self.obtener_jugador()
        self.cant_a.setText(str(jugador.inventario_semillas['semilla_a']))
        self.cant_c.setText(str(jugador.inventario_semillas['semilla_c']))
        [p_actual, p] = self.obtener_paginas()
        self.pags.setText(f'Pag: {p_actual} / {p}')
        p_actual = 'pag' + str(p_actual)
        while len(jugador.inventario_grafico[p_actual]) < 9:
            jugador.inventario_grafico[p_actual].append('')
        for i in range(len(jugador.inventario_grafico[p_actual])):
            obj = jugador.inventario_grafico[p_actual][i]
            img = self.boxes[i]
            if obj == 'semilla_a':
                img = Arrastrable('a', self, 'a')
                pixmap = QPixmap(paths_alcachofa['fase 1'])
            elif obj == 'semilla_c':
                pixmap = QPixmap(paths_choclo['fase 1'])
            elif obj == 'oro':
                pixmap = QPixmap(paths_recursos['oro'])
            elif obj == 'leña':
                pixmap = QPixmap(paths_recursos['leña'])
            elif obj == 'azada':
                pixmap = QPixmap(paths_objetos['azada'])
            elif obj == 'hacha':
                pixmap = QPixmap(paths_objetos['hacha'])
            elif obj == 'alcachofa':
                pixmap = QPixmap(paths_alcachofa['icono'])
            elif obj == 'choclo':
                pixmap = QPixmap(paths_choclo['icono'])
            elif obj == 'ticket':
                pixmap = QPixmap(paths_objetos['ticket'])
            else:
                pixmap = QPixmap('blank.PNG')
            pixmap = pixmap.scaled(N, N)
            img.setPixmap(pixmap)

    def pausar(self):
        self.f_pausar_reanudar.emit()
        if not self.pausado:
            self.timer_general.stop()
            self.pausado = True
            self.boton_pausa.setText('Reanudar')
        else:
            self.timer_general.start()
            self.pausado = False
            self.boton_pausa.setText('Pausar')

    def salir(self):
        self.f_salir.emit()
        self.clear_layout(self.layout_general)
        self.timer_general.stop()
        self.hide()

    def mostrar(self, entidad):
        if entidad.label:
            entidad.label.deleteLater()
        entidad.label = QLabel(self)
        if entidad.key == 'w':
            if entidad._movimiento == 0:
                pixmap = QPixmap(paths_personaje['up_1'])
            elif entidad._movimiento == 1:
                pixmap = QPixmap(paths_personaje['up_2'])
            elif entidad._movimiento == 2:
                pixmap = QPixmap(paths_personaje['up_3'])
            elif entidad._movimiento == 3:
                pixmap = QPixmap(paths_personaje['up_4'])
        elif entidad.key == 'a':
            if entidad._movimiento == 0:
                pixmap = QPixmap(paths_personaje['left_1'])
            elif entidad._movimiento == 1:
                pixmap = QPixmap(paths_personaje['left_2'])
            elif entidad._movimiento == 2:
                pixmap = QPixmap(paths_personaje['left_3'])
            elif entidad._movimiento == 3:
                pixmap = QPixmap(paths_personaje['left_4'])
        elif entidad.key == 's':
            if entidad._movimiento == 0:
                pixmap = QPixmap(paths_personaje['down_1'])
            elif entidad._movimiento == 1:
                pixmap = QPixmap(paths_personaje['down_2'])
            elif entidad._movimiento == 2:
                pixmap = QPixmap(paths_personaje['down_3'])
            elif entidad._movimiento == 3:
                pixmap = QPixmap(paths_personaje['down_4'])
        elif entidad.key == 'd':
            if entidad._movimiento == 0:
                pixmap = QPixmap(paths_personaje['right_1'])
            elif entidad._movimiento == 1:
                pixmap = QPixmap(paths_personaje['right_2'])
            elif entidad._movimiento == 2:
                pixmap = QPixmap(paths_personaje['right_3'])
            elif entidad._movimiento == 3:
                pixmap = QPixmap(paths_personaje['right_4'])
        else:
            pixmap = QPixmap(paths_personaje['down_1'])
        pixmap = pixmap.scaled(P_SIZE, P_SIZE)
        entidad.label.setPixmap(pixmap)
        #print(entidad._x,entidad._y)
        entidad.label.setGeometry(int(entidad._x), int(entidad._y), P_SIZE, P_SIZE)
        entidad.label.show()

        self.timer_general = QTimer()
        self.timer_general.timeout.connect(self.actualizar)
        self.timer_general.start(t)
        self.actualizar_hora_dinero()
        self.actualizar_inventario()
        self.pausado = False

    def cargar_nuevo_mapa(self, mapa):
        ## Mapa
        len_i, len_j = 0, 0
        valores = list()
        with open(mapa, 'r') as file:
            linea = file.readline().strip()
            len_i = len(linea.split(' '))
            while linea:
                len_j += 1
                lista = linea.split(' ')
                valores.append(lista)
                linea = file.readline().strip()
        valores = list(itertools.chain.from_iterable(valores))

        posiciones = list()
        for i in range(len_j):
            for j in range(len_i):
                posiciones.append((i, j))
        self.pos_generales = dict(zip(posiciones, valores))
        self.set_mapa(dict(zip(posiciones, valores)))

    def set_mapa(self, pos_generales):
        posiciones, valores = list(pos_generales.keys()), list(pos_generales.values())

        self.grid = QGridLayout()
        self.grid.setAlignment(Qt.AlignTop)
        jugador = self.obtener_jugador()
        self.pos_casa = list()
        self.pos_tienda = list()
        self.mapa = dict()
        for posicion, valor in zip(posiciones, valores):
            img = QLabel(self)
            if valor == '':
                continue
            elif valor == 'O':
                img.setPixmap(QPixmap(paths_mapa['libre']))
            elif valor == 'C':
                img.setPixmap(QPixmap(paths_mapa['cultivable']))
            elif valor == 'R':
                img.setPixmap(QPixmap(paths_mapa['roca']))
            elif valor == 'H':
                img.setPixmap(QPixmap(paths_mapa['casa']))
                self.pos_casa.append(posicion)
            elif valor == 'T':
                img.setPixmap(QPixmap(paths_mapa['tienda']))
                self.pos_tienda.append(posicion)
            img.setFixedSize(N, N)
            img.setScaledContents(True)
            self.mapa[posicion] = img
            self.grid.addWidget(img, *posicion)
        self.grid.setSpacing(0)

        self.layout_general.setContentsMargins(0, 0, 0, 0)
        self.layout_general.addLayout(self.grid)

        # Casa
        self.casa = QLabel(self)
        self.casa.setPixmap(QPixmap(paths_mapa['casa']).scaled(2*N, 2*N))
        pix_casa = self.transformar_posicion_pixel(self.pos_casa[0])
        self.casa.setGeometry(*pix_casa, 2*N, 2*N)

        # Tienda
        self.tienda = QLabel(self)
        self.tienda.setPixmap(QPixmap(paths_mapa['tienda']).scaled(2*N, 2*N))
        pix_tienda = self.transformar_posicion_pixel(self.pos_tienda[0])
        self.tienda.setGeometry(*pix_tienda, 2*N, 2*N)

        self.f_send_pos.emit(pos_generales)

        ## Barra Lateral
        self.barra_lateral = QVBoxLayout()
        title = QLabel('Stats', self)
        self.barra_lateral.addStretch(1)
        title.setFixedWidth(200)
        self.barra_lateral.addWidget(title, alignment=Qt.AlignTop)
        self.barra_lateral.setAlignment(Qt.AlignTop)

        # Dia, hora y dinero
        [hora, dia] = self.obtener_hora_dia()
        dinero = self.obtener_dinero()
        self.dia = QLabel(f'Día: {dia}', self)
        self.barra_lateral.addWidget(self.dia)
        self.barra_lateral.addStretch(1)
        self.hora = QLabel(f'Hora: {hora}', self)
        self.barra_lateral.addWidget(self.hora)
        self.barra_lateral.addStretch(1)
        self.dinero = QLabel(f'Dinero $: {dinero}', self)
        self.barra_lateral.addWidget(self.dinero)
        self.barra_lateral.addStretch(1)

        # Barra de Energía
        self.barra_lateral.addWidget(QLabel('Energía', self))
        self.energia = QProgressBar()
        self.energia.setValue(jugador.energia)
        self.barra_lateral.addWidget(self.energia)
        self.barra_lateral.addStretch(1)

        # Pausa
        self.boton_pausa = QPushButton('Pausar', self)
        self.boton_pausa.setFixedSize(self.boton_pausa.sizeHint())
        self.boton_pausa.clicked.connect(self.pausar)
        self.barra_lateral.addWidget(self.boton_pausa, alignment = Qt.AlignCenter)

        # Salir
        self.boton_salir = QPushButton('Salir', self)
        self.boton_salir.setFixedSize(self.boton_salir.sizeHint())
        self.boton_salir.clicked.connect(self.salir)
        self.barra_lateral.addWidget(self.boton_salir, alignment = Qt.AlignCenter)

        # Semillas
        self.barra_lateral.addWidget(QLabel('Semillas (arrastre para cultivar)', self))
        self.arrastrables = QHBoxLayout()
        self.arr1 = Arrastrable('a', self, 'a')
        pixmap = QPixmap(paths_alcachofa['semilla'])
        pixmap = pixmap.scaled(N, N)
        self.arr1.pixmap = pixmap
        self.arr1.setPixmap(pixmap)
        self.arrastrables.addWidget(self.arr1)

        self.cant_a = QLabel(str(jugador.inventario_semillas['semilla_a']))
        self.arrastrables.addWidget(self.cant_a)

        self.arr2 = Arrastrable('c', self, 'c')
        pixmap = QPixmap(paths_choclo['semilla'])
        pixmap = pixmap.scaled(N, N)
        self.arr2.pixmap = pixmap
        self.arr2.setPixmap(pixmap)
        self.arrastrables.addWidget(self.arr2)

        self.cant_c = QLabel(str(jugador.inventario_semillas['semilla_c']))
        self.arrastrables.addWidget(self.cant_c)

        self.barra_lateral.addLayout(self.arrastrables)

        # Inventario
        self.barra_lateral.addWidget(QLabel('Inventario', self))
        [p_actual, p] = self.obtener_paginas()
        self.pags = QLabel(f'Pag: {p_actual} / {p}', self)
        self.barra_lateral.addWidget(self.pags)
        
        self.inv = QGridLayout()

        posiciones = [(i, j) for i in range(3) for j in range(3)]
        self.box1 = QLabel(self)
        self.boxes.append(self.box1)
        self.inv.addWidget(self.box1, *posiciones[0])
        self.box2 = QLabel(self)
        self.boxes.append(self.box2)
        self.inv.addWidget(self.box2, *posiciones[1])
        self.box3 = QLabel(self)
        self.boxes.append(self.box3)
        self.inv.addWidget(self.box3, *posiciones[2])
        self.box4 = QLabel(self)
        self.boxes.append(self.box4)
        self.inv.addWidget(self.box4, *posiciones[3])
        self.box5 = QLabel(self)
        self.boxes.append(self.box5)
        self.inv.addWidget(self.box5, *posiciones[4])
        self.box6 = QLabel(self)
        self.boxes.append(self.box6)
        self.inv.addWidget(self.box6, *posiciones[5])
        self.box7 = QLabel(self)
        self.boxes.append(self.box7)
        self.inv.addWidget(self.box7, *posiciones[6])
        self.box8 = QLabel(self)
        self.boxes.append(self.box8)
        self.inv.addWidget(self.box8, *posiciones[7])
        self.box9 = QLabel(self)
        self.boxes.append(self.box9)
        self.inv.addWidget(self.box9, *posiciones[8])
        for posicion, valor in zip(posiciones, valores):
            box = QLabel(self)
            self.inv.addWidget(box, *posicion)
        
        self.barra_lateral.addLayout(self.inv)
        self.barra_lateral.addStretch(1)
        
        self.botones = QHBoxLayout()
        self.boton_der = QPushButton('->')
        self.boton_der.clicked.connect(self.pag_derecha)
        self.boton_izq = QPushButton('<-')
        self.boton_izq.clicked.connect(self.pag_izquierda)
        self.botones.addWidget(self.boton_izq)
        self.botones.addWidget(self.boton_der)

        self.barra_lateral.addLayout(self.botones)

        # Ajuste final
        self.layout_general.addLayout(self.barra_lateral)
        self.setLayout(self.layout_general)
        self.setFixedSize(self.sizeHint())
        self.show()


class Arrastrable(QLabel):
    def __init__(self, title, parent, tipo):
        super().__init__(title, parent)
        self.pixmap = None
        self.tipo = tipo
        
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QPoint(N/2, N/2))
        drag.setPixmap(self.pixmap)
        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
