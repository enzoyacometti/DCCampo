# DCCampo :school_satchel:

## Consideraciones generales :octocat:

* Prioricé la funcionalidad por sobre la estética, pero todo funciona.

* Al comprar o vender en la tienda, el dinero se actualiza constantemente en la ventana de la tienda pero __no se actualiza en la ventana de juego hasta que se salga de la tienda__.

* Las trampas con el teclado se implementaron con ```sets``` por lo que hay que apretar las 3 teclas __simultáneamente__.

* Se cosecha haciendo _click_ sobre la planta.

* Las señales emitidas desde el ```front_end_juego.py``` y ```front_end_inicio.py``` son de la forma ```f_XXX```, las que se emiten desde la ```tienda.py``` son de la forma ```t_XXX``` y las que se emiten desde el ```back_end.py``` son de la forma ```b_XXX```.

* La victoria se obtiene __cuando se termina el día__ en el cual se compra el Gran Ticket.

* Utilice una imagen de color que nombré ```blank.PNG``` que me ayudó a crear un inventario de manera adecuada.

* **¿Qué contiene cada archivo?**
  * ```main.py```: Módulo principal desde donde se corre el programa.
  * ```backend.py```: Módulo que contiene al backend del programa, realiza todas las operaciones "por detrás" de la interfaz.
  * ```entidades.py```: Módulo que contiene a todas las entidades que definí para el programa.
  * ```front_end_inicio.py```: Módulo que contiene el frontend mostrado en la ventana inicial del programa.
  * ```inicio.py```: Módulo que contiene parte del front_end_inicio (cargado del mapa y definición de arrastrable).
  * ```front_end_juego.py```: Módulo que contiene el frontend mostrado durante el desarrollo del juego.
  * ```tienda.py```: Módulo que contiene parte del front_end_juego (_display_ de la tienda).
  * ```parametros_generales.py```: Módulo que contiene los parámetros definidos por mi para el correcto funcionamiento del juego.

* **¿Cómo funciona el programa?**
  * El código de ```main.py``` consiste en:
    * Desde __línea 14__: Definir la aplicación.
    * Desde __línea 16__: Instanciar las entidades ```DCCampo()```, ```VentanaInicio()```, ```VentanaJuego()``` y ```Tienda()```
    * Desde __línea 21__: Relacionar los ```signal_set``` de cada entidad para el traspaso de señales.
    * Desde __línea 26__: Se muestra la ventana de inicio para comenzar el programa.

  * Es relevante decir que para los ```Recursos``` se creó una lista de listas llamada ```tablero_m``` que posee una lista para cada coordenada del grid del mapa, donde agrega los drops que se encuentran ahí (```Oro```, ```Lena```, ```Alcachofa``` y ```Choclo```) los cuales se agregan a dicha lista de listas al definirlos dentro del módulo ```entidades.py```.
  * 

## Ejecución :computer:
* El módulo principal de la tarea a ejecutar es  ```main.py```. 


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```uniform```, ```choice```.
2. ```PyQt5.QtWidgets```: ```QLabel```, ```QWidget```, ```QVBoxLayout```, ```QHBoxLayout```, ```QLineEdit```, ```QPushButton```, ```QGridLayout```, ```QMessageBox```, ```QProgressBar```.
3. ```PyQt5.QtCore```: ```Qt```, ```pyqtSignal```, ```QMimeData```, ```QPoint```.
4.  ```PyQt5.QtGui```: ```QPixmap```, ```QTransform```, ```QDrag```.
5. ```time```: ```sleep```.
6. ```itertools```: ```chain.fromiterable```.
7. ```collections```: ```defaultdict```.
8. ```threading```: ```Thread```.
9. ```os```: ```path.join```.
10. ```functools```: ```partial```.
