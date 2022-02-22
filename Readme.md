# Tarea 2: DCCampo :school_satchel:

## Consideraciones generales :octocat:

* El programa corre bien e implementé __todas__ las funcionalidades mínimas, correrlo no debería ser problema.

* __No implementé__ que los cultivos dejen de crecer cuando se está en pausa.

* Prioricé la funcionalidad por sobre la estética, por lo que no se verá la interfaz como en el enunciado, pero todo funciona.

* Al comprar o vender en la tienda, el dinero se actualiza constantemente en la ventana de la tienda pero __no se actualiza en la ventana de juego hasta que se salga de la tienda__.

* Las trampas con el teclado se implementaron con ```sets``` por lo que hay que apretar las 3 teclas __simultáneamente__.

* Se cosecha haciendo _click_ sobre la planta.

* Las señales emitidas desde el ```front_end_juego.py``` y ```front_end_inicio.py``` son de la forma ```f_XXX```, las que se emiten desde la ```tienda.py``` son de la forma ```t_XXX``` y las que se emiten desde el ```back_end.py``` son de la forma ```b_XXX```.

* La victoria se obtiene __cuando se termina el día__ en el cual se compra el Gran Ticket.

* Utilice una imagen de color que nombré ```blank.PNG``` que me ayudó a crear un inventario de manera adecuada.

* No hice ningún bonus.

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

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos (POO)

* **Ventanas**:
  * _Ventana de inicio_: Se muestra sin superposición y se utiliza la señal ```f_iniciar_juego``` para verificar que el input es válido entre ```front_end_inicio.py``` y ```backend.py```.
  * _Ventana de juego_: Se muestra sin superposición y el ```QTimer``` nombrado ```timer_general``` en la línea 185 de ```inicio.py``` se encarga de actualizar la ventana con los datos (energía y dinero) y al personaje con su posición.
  * _Inventario_: Las semillas se ponen aparte del inventario del jugador por su naturaleza de objetos arrastrables (clase definida en la línea 390 de ```inicio.py``` en base a varias fuentes de internet y documentación de PyQt), donde se usan los métodos ```MousePressEvent```, ```MouseMoveEvent```, ```dragEnterEvent``` y ```dropEvent```.
  * _Tienda_: Se muestra sin superposición y se modifica el dinero directamente del jugador para posteriormente actualizar dicho valor mediante la señal ```t_update_inv``` en las líneas 233 y 250 de ```tienda.py```.
* **Entidades**: 
  * _Jugador_: La entidad ```Jugador``` (línea 7 de ```entidades.py```) posee setters para su movimiento en 'x' y en 'y' que no permite que atraviese rocas o salga del mapa. Como se dijo anteriormente, ```tablero_m``` posee las coordenadas de todos los drops en un instante de tiempo, por lo que el método ```mover_jugador()``` (línea 180 de ```back_end.py```) se ejecuta constantemente revisando si el jugador está parado sobre un drop y, de esta manera, recogerlo.
  * _Recursos_: Se utiliza un ```Thread``` para el crecimiento de cultivos, definido en la línea 339 de ```back_end.py```, el cual identifica el tipo de cultivo y manda una señal con su fase al método ```mostrar_semilla()``` (línea 138 de ```front_end_juego.py```) para mostrarlo en la interfaz. El oro spawnea con el paso de los días, evento que sucede en la línea 113 de ```back_end.py``` y su duración viene dada por el ```Thread``` definido en la línea 311 del mismo módulo (```VidaOro```). Para la leña, spawnea cuando se tala un árbol, donde se gatilla el método ```spawn_lena()``` el cual inicia el thread, que a su vez, manda la señal (la cual se emite en la línea 337 del módulo). Al clickear un árbol, se gatilla el ```MousePressEvent``` en la línea 277 de ```front_end_juego.py```, el cual emite la señal ```f_talar``` conectada con el método ```talar()``` (línea 243 de ```back_end.py```) que inicia el thread de la leña en esa posición. Todas las duraciones de los drops (```Recursos```) vienen dadas por la funcionalidad de ```Threads```.
  * _Herramientas_: Dentro del ```MousePressEvent``` se verifica que en el inventario haya un hacha o una azada antes de realizar una acción determinada.
* **Tiempo**: 
  * _Reloj_: El ```QTimer``` se encarga del transcurso del tiempo, el cual es relativamente acelerado, pero funciona perfectamente y se detiene cuando se pausa el juego. La señal encargada de esto es ```b_entregar_hora_dia``` emitida en la línea 121 de ```back_end.py```.
* **Funcionalidades Extra**: 
  * _KIP_: Se define en el ```keyPressEvent``` (línea 213 de ```front_end_juego.py```) usando ```sets```, la señal encargada de esto es ```f_trampa``` emitida en la línea 223 del mismo método).
  * _MNY_: Se define en el ```keyPressEvent``` (línea 213 de ```front_end_juego.py```) usando ```sets```, la señal encargada de esto es ```f_trampa``` emitida en la línea 226 del mismo método).
  * _Pausa_: La pausa se produce gracias al método ```pausar()``` de ```inicio.py``` el cual está conectado con el botón de pausa del juego. Dicho método emite la señal ```f_pausar_reanudar``` al ```back_end.py```.
* **General**: 
  * _Modularización_: El frontend se compone por: ```inicio.py```, ```front_end_inicio.py```, ```front_end_juego.py``` y ```tienda.py```. El backend se compone por: ```back_end.py```.
  * _Dependencias Circulares_: En ningún módulo del frontend se importa el backend o viceversa.
  * _Parámetros_: El módulo ```parametros_generales.py``` tiene todos los parámetros definidos por mí y se importan dichos valores correctamente a cada módulo.
* **Bonus**: No implementado.

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