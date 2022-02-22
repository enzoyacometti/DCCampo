# Parámetros generales

N = 30

DURACION_LENA = 5
DURACION_ORO = 3

MONEDAS_INICIALES = 100

ENERGIA_JUGADOR = 100
ENERGIA_DORMIR = 30

ENERGIA_PLANTAR = 5

PROB_ARBOL = 0.4
PROB_ORO = 0.1

DINERO_TRAMPA = 500

# Tamaño Personaje
P_SIZE = int(N*0.85)

# Velocidad jugador
VEL_MOVIMIENTO = 350

# Timer rate personaje
TIMER_RATE = 10

PIX_PERIOD = VEL_MOVIMIENTO * (TIMER_RATE / 1000)

t = 10

# PATHS

path_logo = 'sprites/otros/logo'

paths_mapa = {
    'libre': 'sprites/mapa/tile000', 
    'cultivable': 'sprites/mapa/tile061',
    'roca': 'sprites/mapa/tile058',
    'casa': 'sprites/mapa/house',
    'tienda': 'sprites/mapa/store'
}

paths_alcachofa = {
    'icono': 'sprites/cultivos/alcachofa/icon',
    'semilla': 'sprites/cultivos/alcachofa/seeds',
    'fase 1': 'sprites/cultivos/alcachofa/stage_1',
    'fase 2': 'sprites/cultivos/alcachofa/stage_2',
    'fase 3': 'sprites/cultivos/alcachofa/stage_3',
    'fase 4': 'sprites/cultivos/alcachofa/stage_4',
    'fase 5': 'sprites/cultivos/alcachofa/stage_5',
    'fase 6': 'sprites/cultivos/alcachofa/stage_6'
}

paths_choclo = {
    'icono': 'sprites/cultivos/choclo/icon',
    'semilla': 'sprites/cultivos/choclo/seeds',
    'fase 1': 'sprites/cultivos/choclo/stage_1',
    'fase 2': 'sprites/cultivos/choclo/stage_2',
    'fase 3': 'sprites/cultivos/choclo/stage_3',
    'fase 4': 'sprites/cultivos/choclo/stage_4',
    'fase 5': 'sprites/cultivos/choclo/stage_5',
    'fase 6': 'sprites/cultivos/choclo/stage_6',
    'fase 7': 'sprites/cultivos/choclo/stage_7'
}

paths_objetos = {
    'hacha': 'sprites/otros/axe',
    'azada': 'sprites/otros/hoe',
    'inventario': 'sprites/otros/inventary',
    'dinero': 'sprites/otros/money',
    'ticket': 'sprites/otros/ticket',
    'arbol': 'sprites/otros/tree'
}

paths_personaje = {
    'up_1': 'sprites/personaje/up_1',
    'up_2': 'sprites/personaje/up_2',
    'up_3': 'sprites/personaje/up_3',
    'up_4': 'sprites/personaje/up_4',
    'down_1': 'sprites/personaje/down_1',
    'down_2': 'sprites/personaje/down_2',
    'down_3': 'sprites/personaje/down_3',
    'down_4': 'sprites/personaje/down_4',
    'left_1': 'sprites/personaje/left_1',
    'left_2': 'sprites/personaje/left_2',
    'left_3': 'sprites/personaje/left_3',
    'left_4': 'sprites/personaje/left_4',
    'right_1': 'sprites/personaje/right_1',
    'right_2': 'sprites/personaje/right_2',
    'right_3': 'sprites/personaje/right_3',
    'right_4': 'sprites/personaje/right_4'
}

paths_recursos = {
    'oro': 'sprites/recursos/gold',
    'leña': 'sprites/recursos/wood' 
}