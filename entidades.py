from parametros_plantas import (TIEMPO_ALCACHOFAS, TIEMPO_CHOCLOS, FASES_ALCACHOFAS, FASES_CHOCLOS)
from parametros_generales import (DURACION_LENA, DURACION_ORO, PIX_PERIOD, P_SIZE, N, \
    MONEDAS_INICIALES, ENERGIA_JUGADOR)
from random import choice
from collections import defaultdict

class Jugador():
    def __init__(self):
        self._x = None
        self._y = None
        self.inventario_semillas = {'semilla_a': 0, 'semilla_c': 0}
        self.inventario = defaultdict(int)
        self.inventario_grafico = defaultdict(list)
        self.pags = 1
        self.label = None
        self.shop = False
        self.casa = False
        self.energia = ENERGIA_JUGADOR
        self._movimiento = 0
        self.key = None
        self.pos_generales = dict()
        self.dinero = MONEDAS_INICIALES
        self._hora = 0
        self._minutos = 0
        self._dia = 0

    def mover(self, key, pos_generales):
        self.pos_generales = pos_generales
        self.key = key
        self.movimiento += 1
        if self.key == 'w':
            self.pix_y -= PIX_PERIOD
        elif self.key == 'a':
            self.pix_x -= PIX_PERIOD
        elif self.key == 's':
            self.pix_y += PIX_PERIOD
        elif self.key == 'd':
            self.pix_x += PIX_PERIOD
        if self.pix_type(self.pix) == 'T':
            self.shop = True
        elif self.pix_type(self.pix) == 'H':
            self.casa = True

    @property
    def movimiento(self):
        return self._movimiento
    
    @movimiento.setter
    def movimiento(self, valor):
        self._movimiento += 1
        if self._movimiento > 3:
            self._movimiento = 0

    @property
    def pix_x(self):
        return self._x

    @pix_x.setter
    def pix_x(self, valor):
        forb = ('R', 'A')
        lim_pos = list(self.pos_generales.keys())[-1]
        lim_pix_x = self.transformar_posicion_pixel(lim_pos)[0]
        if valor < 0:
            self._x = 0
        elif valor > lim_pix_x:
            self._x = lim_pix_x
        else:
            self._x = valor

        if self.key == 'a':
            if self.pix_type(self.pix) in forb:
                self._x += PIX_PERIOD
            if self.pix_type((self.pix_x, self.pix_y+P_SIZE)) in forb:
                self._x += PIX_PERIOD
        if self.key == 'd':
            if self.pix_type(self.pix) in forb:
                self._x -= PIX_PERIOD
            if self.pix_type((self.pix_x+P_SIZE, self.pix_y)) in forb:
                self._x -= PIX_PERIOD
            if self.pix_type((self.pix_x+P_SIZE, self.pix_y+P_SIZE)) in forb:
                self._x -= PIX_PERIOD

    @property
    def pix_y(self):
        return self._y
    
    @pix_y.setter
    def pix_y(self, valor):
        forb = ('R', 'A')
        lim_pos = list(self.pos_generales.keys())[-1]
        lim_pix_y = self.transformar_posicion_pixel(lim_pos)[1]
        if valor < 0:
            self._y = 0
        elif valor > lim_pix_y:
            self._y = lim_pix_y
        else:
            self._y = valor

        if self.key =='w':
            if self.pix_type(self.pix) in forb:
                self._y += PIX_PERIOD
            if self.pix_type((self.pix_x+P_SIZE, self.pix_y)) in forb:
                self._y += PIX_PERIOD
        if self.key == 's':
            if self.pix_type(self.pix) in forb:
                self._y -= PIX_PERIOD
            if self.pix_type((self.pix_x, self.pix_y+P_SIZE)) in forb:
                self._y -= PIX_PERIOD
            if self.pix_type((self.pix_x+P_SIZE, self.pix_y+P_SIZE)) in forb:
                self._y -= PIX_PERIOD

    @property
    def pos(self):
        pos_y = int((self.pix_y) // N)
        pos_x = int((self.pix_x) // N)
        return (pos_y, pos_x)
    
    def pos_type(self, pos):
        return self.pos_generales[pos]

    @property
    def pix(self):
        return (self.pix_x, self.pix_y)

    def pix_type(self, pix):
        pos_x = int(pix[0] // N)
        pos_y = int(pix[1] // N)
        return self.pos_type((pos_y, pos_x))

    @property
    def dar_hora(self):
        return self._hora

    @dar_hora.setter
    def dar_hora(self, valor):
        self._hora += 1
        if self._hora > 23:
            self._hora = 0
            self._dia += 1

    @property
    def dar_minutos(self):
        return self._minutos

    @dar_minutos.setter
    def dar_minutos(self, valor):
        self._minutos += 1
        if self._minutos > 59:
            self._minutos = 0
            self.dar_hora += 1

    def transformar_posicion_pixel(self, posicion):
        posicion = (posicion[0], posicion[1])
        pixel = tuple(map(lambda x: x*N, posicion))[::-1]
        return pixel

class Casa():
    def __init__(self):
        self.pos = list()

class Cultivo():

    def __init__(self, pos, tablero):
        self.perm = None
        self.fase = 0
        self.label = None
        self.pos = pos
        self.age = 1

class CultivoAlcachofa(Cultivo):

    def __init__(self, pos, tablero):
        super().__init__(pos, tablero)
        self.perm = False
        self.tiempo = int(TIEMPO_ALCACHOFAS)
        self.fases_totales = int(FASES_ALCACHOFAS)
        self.tipo = 'a'


class CultivoChoclo(Cultivo):

    def __init__(self, pos, tablero):
        super().__init__(pos, tablero)
        self.perm = True
        self.tiempo = int(TIEMPO_CHOCLOS)
        self.fases_totales = int(FASES_CHOCLOS)
        self.tipo = 'c'

class Recurso():

    def __init__(self, pos_generales, tablero):
        super().__init__()
        self.tiempo = None
        self.pos = None

class Alcachofa(Recurso):

    def __init__(self, pos_generales, tablero, pos):
        super().__init__(pos_generales, tablero)
        self.pos = pos
        tablero[pos[0]][pos[1]].append(self)
        self.label = None
        self.tipo = 'alcachofa'

class Choclo(Recurso):

    def __init__(self, pos_generales, tablero, pos):
        super().__init__(pos_generales, tablero)
        self.pos = pos
        tablero[pos[0]][pos[1]].append(self)
        self.label = None
        self.tipo = 'choclo'


class Lena(Recurso):

    def __init__(self, pos_generales, tablero, pos):
        super().__init__(pos_generales, tablero)
        self.pos = pos
        tablero[pos[0]][pos[1]].append(self)
        self.tiempo = DURACION_LENA
        self.label = None
        self.tipo = 'l'

class Oro(Recurso):

    def __init__(self, pos_generales, tablero):
        super().__init__(pos_generales, tablero)
        pos = choice(list(pos_generales.keys()))
        while (pos_generales[pos] not in ('O') \
            and not tablero[pos[0]][pos[1]]):
             pos = choice(list(pos_generales.keys()))
        tablero[pos[0]][pos[1]].append(self)
        self.pos = pos
        self.tiempo = DURACION_ORO
        self.label = None
        self.tipo = 'o'

class Arbol():

    def __init__(self, pos_generales, tablero):
        self.era = None
        pos = choice(list(pos_generales.keys()))
        while (pos_generales[pos] not in ('O') and not tablero[pos[0]][pos[1]]):
            pos = choice(list(pos_generales.keys()))
        tablero[pos[0]][pos[1]].append(self)
        self.era = pos
        pos_generales[pos] = 'A'
        self.pos = pos
        self.label = None
        self.tiempo = 0
        self.tipo = 'arbol'