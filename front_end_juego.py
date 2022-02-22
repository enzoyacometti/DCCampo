from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
                            QLineEdit, QPushButton, QGridLayout, QMessageBox,\
                            QProgressBar)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData, QPoint
from PyQt5.QtGui import QPixmap, QTransform, QDrag
import time
import random
import itertools
from collections import defaultdict
from parametros_acciones import ENERGIA_HERRAMIENTA
from parametros_generales import N, P_SIZE, t, ENERGIA_JUGADOR, DURACION_ORO, \
    DURACION_LENA, paths_mapa, paths_alcachofa, paths_choclo, paths_objetos, \
        paths_personaje, paths_recursos
from parametros_precios import PRECIO_ALACACHOFAS, PRECIO_AZADA, PRECIO_CHOCLOS, \
    PRECIO_HACHA, PRECIO_LEÑA, PRECIO_ORO, PRECIO_SEMILLA_ALCACHOFAS, \
        PRECIO_SEMILLA_CHOCLOS, PRECIO_TICKET
from entidades import Recurso, Arbol, Oro, Jugador, Cultivo, CultivoAlcachofa, CultivoChoclo, \
    Alcachofa, Choclo
from inicio import Arrastrable, CargarMapa

class VentanaJuego(QWidget, CargarMapa):

    f_send_pos = pyqtSignal(dict)
    f_send_key = pyqtSignal(str)
    f_trampa = pyqtSignal(str)
    f_plantar_semilla = pyqtSignal(str, tuple, Jugador)
    f_talar = pyqtSignal(tuple, Arbol)
    f_obtener_tablero = pyqtSignal()
    f_cosechar = pyqtSignal(Recurso, Cultivo, tuple)
    f_update_pos_tablero = pyqtSignal(list)
    f_gasto_energia = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('DCCampo')
        self.str_cheat = set()

    def signal_set(self, juego, tienda):
        juego.b_juego_iniciado.connect(self.cargar_nuevo_mapa)
        juego.b_entregar_dinero.connect(self.return_obtenido)
        juego.b_entregar_hora_dia.connect(self.return_obtenido)
        juego.b_mostrar.connect(self.mostrar)
        juego.b_gasto_energia.connect(self.mostrar_energia)
        juego.b_message_box.connect(self.message_box)
        juego.b_mostrar_semilla.connect(self.mostrar_semilla)
        juego.b_spawn_oro.connect(self.mostrar_oro)
        juego.b_spawn_arbol.connect(self.mostrar_arbol)
        juego.b_restaurar_energia.connect(self.mostrar_energia)
        juego.b_update_inv.connect(self.update_inv)
        juego.b_entregar_paginas.connect(self.return_obtenido)
        juego.b_entregar_jugador.connect(self.return_obtenido)
        juego.b_fin.connect(self.message_box)
        juego.b_start_stop.connect(self.start_stop)
        juego.b_entregar_tablero.connect(self.return_obtenido)
        juego.b_spawn_lena.connect(self.mostrar_lena)
        juego.b_act_pos.connect(self.update_pos_generales)
        juego.b_mostrar_cosecha.connect(self.mostrar_cosecha)
        juego.b_casa.connect(self.message_box)
        juego.b_send_key_none.connect(self.clear_key)

        tienda.t_update_inv.connect(self.update_inv)        

    def update_inv(self, jugador, pag_actual):
        list_inv = list()
        for obj in jugador.inventario:
            n = int(jugador.inventario[obj])
            for _ in range(n):
                list_inv.append(obj)
        jugador.pags = int(len(list_inv)//9 + 1)
        jugador.inventario_grafico = defaultdict(list)
        for i in range(jugador.pags):
            num = 'pag' + str(i+1)
            if (i+1) != jugador.pags:
                m = 9
            else:
                m = int(len(list_inv)%9)
            if m != 0:
                if m == 9:
                    for j in range(9*i, 9*i + 9):
                        jugador.inventario_grafico[num].append(list_inv[j])
                else:
                    for j in range(1, m+1):
                        jugador.inventario_grafico[num].append(list_inv[j-m-1])
            else:
                for _ in range(9):
                    jugador.inventario_grafico[num].append('')

    def update_pos_generales(self, pos_generales):
        self.pos_generales = pos_generales

    def mostrar_energia(self, nva_e):
        if nva_e == 'cheat':
            self.energia.setValue(100)
        else:
            self.energia.setValue(nva_e)

    def mostrar_oro(self, oro, bul):
        if bul:
            pix_x, pix_y = self.transformar_posicion_pixel(oro.pos)
            oro.label = QLabel(self)
            pixmap = QPixmap(paths_recursos['oro'])
            pixmap = pixmap.scaled(N, N)
            oro.label.setPixmap(pixmap)
            oro.label.setGeometry(pix_x, pix_y, N, N)
            oro.label.show()
        else:
            if oro.label:
                oro.label.deleteLater()
    
    def mostrar_arbol(self, arbol, bul):
        if bul:
            pix_x, pix_y = self.transformar_posicion_pixel(arbol.pos)
            arbol.label = QLabel(self)
            pixmap = QPixmap(paths_objetos['arbol'])
            pixmap = pixmap.scaled(N, N)
            arbol.label.setPixmap(pixmap)
            arbol.label.setGeometry(pix_x, pix_y, N, N)
            arbol.label.show()
        else:
            if arbol.label:
                arbol.label.deleteLater()

    def mostrar_lena(self, lena, bul):
        if bul:
            pix_x, pix_y = self.transformar_posicion_pixel(lena.pos)
            lena.label = QLabel(self)
            pixmap = QPixmap(paths_recursos['leña'])
            pixmap = pixmap.scaled(N, N)
            lena.label.setPixmap(pixmap)
            lena.label.setGeometry(pix_x, pix_y, N, N)
            lena.label.show()
        else:
            lena.label.deleteLater()

    def mostrar_semilla(self, cultivo, path, bul):
        if bul:
            if cultivo.label:
                cultivo.label.deleteLater()
            cultivo.label = QLabel(self)
            pix = self.transformar_posicion_pixel(cultivo.pos)
            cultivo.label.setGeometry(*pix, N, N)
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(N, N)
            cultivo.label.setPixmap(pixmap)
            cultivo.label.show()
        else:
            cultivo.label.deleteLater()
    
    def mostrar_cosecha(self, cosecha, bul):
        if bul: 
            pix_x, pix_y = self.transformar_posicion_pixel(cosecha.pos)
            img_cosecha = QLabel(self)
            cosecha.label = img_cosecha
            if cosecha.tipo == 'alcachofa':
                pixmap = QPixmap(paths_alcachofa['icono'])
            else:
                pixmap = QPixmap(paths_choclo['icono'])
            pixmap = pixmap.scaled(N, N)
            img_cosecha.setPixmap(pixmap)
            img_cosecha.setGeometry(pix_x, pix_y, N, N)
            print('mostrando cosecha...')
            img_cosecha.show()
        else:
            cosecha.label.deleteLater()

    def message_box(self, text):
        if text == 'fin':
            mensaje = QMessageBox(self)
            mensaje.setText('¡Victoria!\n¡Ha conseguido El Gran Ticket de regreso al DCC!')
            mensaje.setWindowTitle('DCCampo')
            mensaje.addButton(QMessageBox.Ok)
            mensaje.show()
            self.salir()
        elif text == 'loss':
            mensaje = QMessageBox(self)
            mensaje.setText('¡Derrota!\n¡Te has quedado sin energía!')
            mensaje.setWindowTitle('DCCampo')
            mensaje.addButton(QMessageBox.Ok)
            mensaje.show()
            self.salir()
        else:
            mensaje = QMessageBox(self)
            mensaje.setText(text)
            mensaje.setWindowTitle('DCCampo')
            mensaje.addButton(QMessageBox.Ok)
            mensaje.show()
        

    def start_stop(self, jugador, inicio):
        if self.timer_general.isActive():
            self.timer_general.stop()
        else:
            pix_x, pix_y = self.transformar_posicion_pixel(inicio)
            jugador._x = pix_x
            jugador._y = pix_y
            self.key_pressed = None
            self.timer_general.start()
            self.mostrar(jugador)
    
    def obtener_tablero(self):
        self.f_obtener_tablero.emit()
        return self.obtenido

    def transformar_posicion_pixel(self, posicion):
        # Solo para objetos no móviles
        posicion = (posicion[0], posicion[1])
        pixel = tuple(map(lambda x: x*N, posicion))[::-1]
        return pixel    

    def keyPressEvent(self, event):
        if not self.key_pressed:
            self.key_pressed = event.text()
        if event.text():
            self.str_cheat.add(event.text())
            set_kip = {'k', 'i', 'p'}
            set_mny = {'m', 'n', 'y'}
            if len(self.str_cheat) > 3:
                self.str_cheat = set()
            if len(set_kip & self.str_cheat) == 3:
                self.f_trampa.emit('kip')
                self.str_cheat = set()
            if len(set_mny & self.str_cheat) == 3:
                self.f_trampa.emit('mny')
                self.str_cheat = set()
    
    def keyReleaseEvent(self, event):
        if self.key_pressed in self.str_cheat:
            self.str_cheat.remove(self.key_pressed)
        if self.key_pressed:
            self.key_pressed = None

    def dragEnterEvent(self, e):
        e.accept()
    
    def dropEvent(self, e):
        pos = (int(e.pos().y()//N), int(e.pos().x()//N))
        jugador = self.obtener_jugador()
        self.f_plantar_semilla.emit(e.source().tipo, pos, jugador)
        e.setDropAction(Qt.MoveAction)
        e.accept()

    def mousePressEvent(self, event):
        pos = (int(event.y()//N), int(event.x()//N))
        jugador = self.obtener_jugador()
        tablero = self.obtener_tablero()
        if pos[1] > 20:
            pass
        elif self.pos_generales[pos] == 'C':
            lugar = tablero[pos[0]][pos[1]]
            if len(lugar) > 0:
                for obj in lugar:
                    if obj.tipo == 'a' or obj.tipo == 'c':
                        if obj.age == obj.fases_totales:
                            if obj.tipo == 'a':
                                alcachofa = Alcachofa(self.pos_generales, tablero, pos)
                                self.f_update_pos_tablero.emit(tablero)
                                self.f_cosechar.emit(alcachofa, obj, pos)
                            elif obj.tipo == 'c':
                                choclo = Choclo(self.pos_generales, tablero, pos)
                                self.f_update_pos_tablero.emit(tablero)
                                self.f_cosechar.emit(choclo, obj ,pos)
        elif self.pos_generales[pos] == 'O':
            if jugador.inventario['azada'] > 0:
                self.f_gasto_energia.emit(ENERGIA_HERRAMIENTA)
                self.pos_generales[pos] = 'C'
                self.f_send_pos.emit(self.pos_generales)
                img = self.mapa[pos]
                img.setPixmap(QPixmap(paths_mapa['cultivable']))
                img.setFixedSize(N, N)
                img.setScaledContents(True)
                self.mapa[pos] = img
            else:
                self.message_box('No posee azada para arar')
        elif self.pos_generales[pos] == 'A':
            self.f_gasto_energia.emit(ENERGIA_HERRAMIENTA)
            for obj in tablero[pos[0]][pos[1]]:
                if obj.tipo == 'arbol':
                    arbol = obj
            if jugador.inventario['hacha'] > 0:
                self.f_talar.emit(pos, arbol)
            else:
                self.message_box('No posee hacha para talar')
    
    def clear_key(self):
        self.key_pressed = None

    def clear_layout(self, layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())
