from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QLabel
from entidades import Recurso, Jugador, Cultivo, CultivoAlcachofa, CultivoChoclo, Casa, Arbol, \
    Oro, Lena
from parametros_generales import N, P_SIZE, MONEDAS_INICIALES, PROB_ARBOL, PROB_ORO, \
    DURACION_LENA, DURACION_ORO, DINERO_TRAMPA, paths_alcachofa, paths_choclo, \
        ENERGIA_DORMIR, ENERGIA_PLANTAR
from parametros_plantas import TIEMPO_ALCACHOFAS, TIEMPO_CHOCLOS, FASES_ALCACHOFAS, \
    FASES_CHOCLOS, COSECHA_ALCACHOFAS, COSECHA_CHOCLOS
from parametros_acciones import ENERGIA_COSECHAR, ENERGIA_HERRAMIENTA, ENERGIA_RECOGER
from threading import Thread
import random
import time
import os

class DCCampo(QObject):

    b_entregar_mapa = pyqtSignal(str)
    b_mensaje_inicio = pyqtSignal(str)
    b_juego_iniciado = pyqtSignal(str)
    b_entregar_hora_dia = pyqtSignal(list)
    b_entregar_dinero = pyqtSignal(int)
    b_chao_inicio = pyqtSignal()
    b_mostrar = pyqtSignal(Jugador)
    b_gasto_energia = pyqtSignal(int)
    b_message_box = pyqtSignal(str)
    b_mostrar_semilla = pyqtSignal(Cultivo, str, bool)
    b_spawn_oro = pyqtSignal(Oro, bool)
    b_spawn_arbol = pyqtSignal(Arbol, bool)
    b_spawn_lena = pyqtSignal(Lena, bool)
    b_restaurar_energia = pyqtSignal(str)
    b_update_inv = pyqtSignal(Jugador, int)
    b_entregar_paginas = pyqtSignal(list)
    b_entregar_jugador = pyqtSignal(Jugador)
    b_entregar_tablero = pyqtSignal(list)
    b_fin = pyqtSignal(str)
    b_open_shop = pyqtSignal(Jugador)
    b_start_stop = pyqtSignal(Jugador, tuple)
    b_act_pos = pyqtSignal(dict)
    b_mostrar_cosecha = pyqtSignal(Recurso, bool)
    b_casa = pyqtSignal(str)
    b_send_key_none = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.mapa = ''
        self.jugador = Jugador()
        self.casa = Casa()
        self.pausado = False
        self.tablero_m = None
        self.pos_generales = dict()
        self.hora = ['0', '0', ':', '0', '0']
        self.pag_actual = 1
        self.inicio = None

    def signal_set(self, ventana_inicio, ventana_juego, tienda):
        ventana_inicio.f_iniciar_juego.connect(self.iniciar_juego)

        ventana_juego.f_send_pos.connect(self.set_pos_generales)
        ventana_juego.f_obtener_hora_dia.connect(self.entregar_hora_dia)
        ventana_juego.f_obtener_dinero.connect(self.entregar_dinero)
        ventana_juego.f_pausar_reanudar.connect(self.pausar)
        ventana_juego.f_salir.connect(self.salir)
        ventana_juego.f_pag_der.connect(self.pag_derecha)
        ventana_juego.f_pag_izq.connect(self.pag_izquierda)
        ventana_juego.f_send_key.connect(self.mover_jugador)
        ventana_juego.f_trampa.connect(self.trampa)
        ventana_juego.f_plantar_semilla.connect(self.plantar_semilla)
        ventana_juego.f_obtener_paginas.connect(self.entregar_paginas)
        ventana_juego.f_obtener_jugador.connect(self.entregar_jugador)
        ventana_juego.f_talar.connect(self.talar)
        ventana_juego.f_obtener_tablero.connect(self.entregar_tablero)
        ventana_juego.f_cosechar.connect(self.cosechar)
        ventana_juego.f_update_pos_tablero.connect(self.update_tablero)
        ventana_juego.f_gasto_energia.connect(self.gastar_energia)

        tienda.t_back_game.connect(self.back_game)
        tienda.t_buscar_jugador.connect(self.entregar_jugador)
        tienda.t_obtener_paginas.connect(self.entregar_paginas)

    def entregar_jugador(self):
        self.b_entregar_jugador.emit(self.jugador)
    
    def entregar_mapa(self):
        self.b_entregar_mapa.emit(self.mapa)

    def entregar_tablero(self):
        self.b_entregar_tablero.emit(self.tablero_m)

    def entregar_paginas(self):
        self.b_entregar_paginas.emit([self.pag_actual, self.jugador.pags])

    def entregar_hora_dia(self):
        dia_pre = self.jugador._dia
        self.jugador.dar_minutos += 1
        dia_post = self.jugador._dia
        horas = str(self.jugador._hora)
        mins = str(self.jugador._minutos)
        if len(horas) > 1:
            self.hora[0] = str(horas[0])
            self.hora[1] = str(horas[1])
        elif len(horas) == 1:
            self.hora[0] = '0'
            self.hora[1] = str(horas)
        if len(mins) > 1:
            self.hora[3] = str(mins[0])
            self.hora[4] = str(mins[1])
        elif len(mins) == 1:
            self.hora[3] = '0'
            self.hora[4] = str(mins)
        hora_oficial = ''.join(self.hora)
        if dia_pre < dia_post:
            arbol = Arbol(self.pos_generales, self.tablero_m)
            self.spawn_arbol(arbol)
            self.b_act_pos.emit(self.pos_generales)
            oro = Oro(self.pos_generales, self.tablero_m)
            self.spawn_oro(oro)
            if 'ticket' in self.jugador.inventario.keys():
                self.b_fin.emit('fin')
        self.b_entregar_hora_dia.emit([hora_oficial, self.jugador._dia])

    def update_tablero(self, tablero):
        self.tablero_m = tablero

    def gastar_energia(self, gasto):
        if gasto == 0:
            self.jugador.energia = 100
        else:
            self.jugador.energia -= gasto
        self.b_gasto_energia.emit(self.jugador.energia)

    def entregar_dinero(self):
        self.b_entregar_dinero.emit(self.jugador.dinero)

    def iniciar_juego(self, mapa):
        ruta = os.path.join('mapas', mapa)
        if not os.path.isfile(ruta):
            error = 'Mapa inválido\nPor favor intente nuevamente'
            self.b_mensaje_inicio.emit(error)
        else:
            self.mapa += ruta
            self.b_chao_inicio.emit()
            self.b_juego_iniciado.emit(self.mapa)
            casa = self.casa.pos
            opcs = [(casa[0][0]-1, casa[0][1]), (casa[0][0], casa[0][1]-1),
                    (casa[1][0]-1, casa[1][1]), (casa[1][0], casa[1][1]+1),
                    (casa[2][0]+1, casa[2][1]), (casa[2][0], casa[2][1]-1),
                    (casa[3][0]+1, casa[3][1]), (casa[3][0], casa[3][1]+1)]
            for opc in opcs:
                if self.pos_generales[opc] == 'O':
                    self.inicio = opc
            pix_x, pix_y = self.transformar_posicion_pixel(self.inicio)
            self.jugador._x = pix_x
            self.jugador._y = pix_y
            self.b_mostrar.emit(self.jugador)

    def pausar(self):
        if not self.pausado:
            self.pausado = True
        else:
            self.pausado = False

    def set_pos_generales(self, pos_generales):
        self.pos_generales = pos_generales
        pos_casa = list()
        pos_tienda = list()
        for pos in self.pos_generales:
            if self.pos_generales[pos] == 'H':
                pos_casa.append(pos)
            elif self.pos_generales[pos] == "T":
                pos_tienda.append(pos)
        self.casa.pos = pos_casa
        self.jugador.pos_generales = pos_generales

        lim_y, lim_x = list(self.pos_generales.keys())[-1]
        self.tablero_m = \
                [[list() for _ in range(lim_x+1)] for _ in range(lim_y+1)]

    def mover_jugador(self, key):
        self.jugador.mover(key, self.pos_generales)
        self.b_mostrar.emit(self.jugador)
        pix = (self.jugador.pix_x+P_SIZE/2, self.jugador.pix_y+P_SIZE/2)
        pos = (int(pix[1]//N), int(pix[0]//N))
        if len(self.tablero_m[pos[0]][pos[1]]) > 0:
            for i in range(len(self.tablero_m[pos[0]][pos[1]])):
                if self.tablero_m[pos[0]][pos[1]][i].tipo == 'o':
                    self.b_spawn_oro.emit(self.tablero_m[pos[0]][pos[1]][i], False)
                    self.tablero_m[pos[0]][pos[1]].clear()
                    self.jugador.inventario['oro'] += 1
                    self.b_update_inv.emit(self.jugador, self.pag_actual)
                    self.gastar_energia(ENERGIA_RECOGER)
                elif self.tablero_m[pos[0]][pos[1]][i].tipo == 'l':
                    self.b_spawn_lena.emit(self.tablero_m[pos[0]][pos[1]][i], False)
                    self.tablero_m[pos[0]][pos[1]].clear()
                    self.jugador.inventario['leña'] += 1
                    self.b_update_inv.emit(self.jugador, self.pag_actual)
                    self.gastar_energia(ENERGIA_RECOGER)
                elif self.tablero_m[pos[0]][pos[1]][i].tipo == 'alcachofa':
                    self.b_mostrar_cosecha.emit(self.tablero_m[pos[0]][pos[1]][i], False)
                    self.tablero_m[pos[0]][pos[1]].clear()
                    self.jugador.inventario['alcachofa'] += 1
                    self.b_update_inv.emit(self.jugador, self.pag_actual)
                    self.gastar_energia(ENERGIA_RECOGER)
                elif self.tablero_m[pos[0]][pos[1]][i].tipo == 'choclo':
                    self.b_mostrar_cosecha.emit(self.tablero_m[pos[0]][pos[1]][i], False)
                    self.tablero_m[pos[0]][pos[1]].clear()
                    self.jugador.inventario['choclo'] += 1
                    self.b_update_inv.emit(self.jugador, self.pag_actual)
                    self.gastar_energia(ENERGIA_RECOGER)
            

        if self.jugador.shop:
            self.b_open_shop.emit(self.jugador)
            self.b_start_stop.emit(self.jugador, self.inicio)

        if self.jugador.casa:
            self.jugador.casa = False
            self.jugador.energia += ENERGIA_DORMIR
            self.jugador._dia += 1
            pix_x, pix_y = self.transformar_posicion_pixel(self.inicio)
            self.jugador._x = pix_x
            self.jugador._y = pix_y
            self.b_send_key_none.emit()
            self.b_casa.emit('¡Ha pasado un día y tu energía se ha recargado!')
            self.b_mostrar.emit(self.jugador)

    def spawn_arbol(self, arbol):
        prob = random.uniform(0, 1)
        if prob < PROB_ARBOL:
            self.b_spawn_arbol.emit(arbol, True)

    def spawn_oro(self, oro):
        prob = random.uniform(0, 1)
        if prob < PROB_ORO:
            vida_oro = VidaOro(self.b_spawn_oro, oro, self.tablero_m)
            vida_oro.start()

    def spawn_lena(self, lena):
        vida_lena = VidaLena(self.b_spawn_lena, lena, self.tablero_m)
        vida_lena.start()

    def talar(self, pos, arbol):
        self.pos_generales[pos] = str(arbol.era)
        self.tablero_m[pos[0]][pos[1]].clear()
        self.b_spawn_arbol.emit(arbol, False)
        lena = Lena(self.pos_generales, self.tablero_m, arbol.era)
        self.spawn_lena(lena)

    def cosechar(self, recurso, cultivo, pos):
        if cultivo.perm:
            cultivo.age = cultivo.fases_totales - 1
            crec = CrecimientoCultivo(cultivo, self.tablero_m, self.b_mostrar_semilla)
            crec.start()
        else:
            for obj in self.tablero_m[pos[0]][pos[1]]:
                if obj.tipo == 'a':
                    self.tablero_m[pos[0]][pos[1]].remove(obj)
            self.b_mostrar_semilla.emit(cultivo, '', False)
        print('emit para mostrar cosecha...')
        self.b_mostrar_cosecha.emit(recurso, True)

    def plantar_semilla(self, tipo, pos, jugador):
        if self.pos_generales[pos] != 'C':
            ms = 'El lugar elegido no es válido.\nDebe ser un espacio cultivable.'
            return self.b_message_box.emit(ms)
        if tipo == 'a':
            if jugador.inventario_semillas['semilla_a'] == 0:
                ms = 'No posee semillas de alcachofa.'
                return self.b_message_box.emit(ms)
            alcachofa = CultivoAlcachofa(pos, self.tablero_m)
            crec = CrecimientoCultivo(alcachofa, self.tablero_m, self.b_mostrar_semilla)
            jugador.inventario_semillas['semilla_a'] -= 1
        elif tipo == 'c':
            if jugador.inventario_semillas['semilla_c'] == 0:
                ms = 'No posee semillas de choclo.'
                return self.b_message_box.emit(ms)
            choclo = CultivoChoclo(pos, self.tablero_m)
            crec = CrecimientoCultivo(choclo, self.tablero_m, self.b_mostrar_semilla)
            jugador.inventario_semillas['semilla_c'] -= 1
        self.gastar_energia(ENERGIA_PLANTAR)
        crec.start()

    def pag_derecha(self):
        if self.pag_actual < self.jugador.pags:
            self.pag_actual += 1

    def pag_izquierda(self):
        if self.pag_actual > 1:
            self.pag_actual -= 1

    def back_game(self):
        self.b_start_stop.emit(self.jugador, self.inicio)

    def transformar_posicion_pixel(self, posicion):
        # Solo para objetos no móviles
        posicion = (posicion[0], posicion[1])
        pixel = tuple(map(lambda x: x*N, posicion))[::-1]
        return pixel 

    def salir(self):
        self.mapa = None
        self.dinero = 0

    def trampa(self, tipo):
        if tipo == 'kip':
            self.gastar_energia(0)
        elif tipo == 'mny':
            self.jugador.dinero += DINERO_TRAMPA

class VidaOro(Thread):
    def __init__(self, spawn_oro, oro, tablero, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spawn_oro = spawn_oro
        self.oro = oro
        [self.x, self.y] = oro.pos 
        self.tablero = tablero

    def run(self):
        self.spawn_oro.emit(self.oro, True)
        time.sleep(DURACION_ORO)
        if len(self.tablero[self.x][self.y]) > 0:
            self.spawn_oro.emit(self.oro, False)

class VidaLena(Thread):
    def __init__(self, spawn_lena, lena, tablero, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spawn_lena = spawn_lena
        self.lena = lena
        [self.x, self.y] = lena.pos 
        self.tablero = tablero

    def run(self):
        self.spawn_lena.emit(self.lena, True)
        time.sleep(DURACION_LENA)
        if len(self.tablero[self.x][self.y]) > 0:
            self.spawn_lena.emit(self.lena, False)

class CrecimientoCultivo(Thread):
    def __init__(self, cultivo, tablero, mostrar_semilla, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cultivo = cultivo
        self.tablero = tablero
        self.mostrar_semilla = mostrar_semilla

    def run(self):
        while self.cultivo.age <= self.cultivo.fases_totales:
            if self.cultivo.tipo == 'a':
                fase = 'fase ' + str(self.cultivo.age)
                path = paths_alcachofa[fase]
                self.mostrar_semilla.emit(self.cultivo, path, True)
                time.sleep(TIEMPO_ALCACHOFAS/25)
            elif self.cultivo.tipo == 'c':
                fase = 'fase ' + str(self.cultivo.age)
                path = paths_choclo[fase]
                self.mostrar_semilla.emit(self.cultivo, path, True)
                time.sleep(TIEMPO_CHOCLOS/100)
            if self.cultivo.age == self.cultivo.fases_totales:
                break
            self.cultivo.age += 1
        self.tablero[self.cultivo.pos[0]][self.cultivo.pos[1]].append(self.cultivo)       
