from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
                            QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import os
from parametros_generales import path_logo


class VentanaInicio(QWidget):

    f_iniciar_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_gui()
        
    def init_gui(self):
        self.setGeometry(450, 100, 300, 300)
        self.setWindowTitle('DCCampo')

        self.layout_general = QHBoxLayout()
        self.setLayout(self.layout_general)

        self.mostrar_inicio()
    
    def signal_set(self, juego, ventana_juego):
        juego.b_mensaje_inicio.connect(self.mostrar_mensaje_inicio)
        juego.b_chao_inicio.connect(self.chao)

        ventana_juego.f_salir.connect(self.mostrar_inicio)

    def mostrar_inicio(self):
        self.layout_general.addStretch(1)

        # Vertical General
        vbox_general = QVBoxLayout()

        self.logo = QLabel(self)
        self.logo.setGeometry(50, 50, 100, 100)
        pixeles = QPixmap(path_logo)
        self.logo.setPixmap(pixeles)
        self.logo.setScaledContents(True)

        vbox_general.addWidget(self.logo)
        vbox_general.addWidget(QLabel('Ingresa el nombre de mapa a cargar (con extensión .txt):',\
             self), alignment=Qt.AlignCenter)

        # Campo Editable
        self.campo = QLineEdit('', self)
        self.campo.returnPressed.connect(self.iniciar_juego)
        self.campo.setFixedWidth(200)
        hbox = QHBoxLayout()
        hbox.addWidget(self.campo)
        vbox_general.addLayout(hbox)
        
        # Boton
        boton_inicio = QPushButton('Jugar', self)
        boton_inicio.setFixedSize(boton_inicio.sizeHint())
        boton_inicio.clicked.connect(self.iniciar_juego)
        vbox_general.addWidget(boton_inicio, alignment=Qt.AlignCenter)
        vbox_general.setAlignment(Qt.AlignCenter)

        # Setear Mensaje
        self.mensaje_inicio = QLabel('', self)
        vbox_general.addWidget(self.mensaje_inicio, alignment=Qt.AlignCenter)
        
        # Ajustes Finales
        self.layout_general.addLayout(vbox_general)
        self.layout_general.setAlignment(Qt.AlignCenter)
        self.layout_general.addStretch(1)

    def iniciar_juego(self):
        mapa = self.campo.text()
        self.f_iniciar_juego.emit(mapa)

    def chao(self):
        self.hide()

    def mostrar_mensaje_inicio(self, mensaje):
        self.mensaje_inicio.setText(mensaje)