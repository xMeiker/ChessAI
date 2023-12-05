# Chess With AI
*  Inspirado por **Eddie Sharick**
* Editado y Actualizado por **xMeiker**
* Nuevas Funciones y Menu Custom por **xMeiker**
<p align="center"><img src="imagesBG/menuBK.jpg" width="1920px" height="360px" alt="title"></p>

## Tabla de Contenido
* [Info General](##general-info)
* [Tecnologias](#technologies)
* [Cosas por implementar o mejoras](#todo)
* [Instrucciones](#instructions)
* [Otras ideas de desarrollo](#further-development-ideas)

## Info General
Este proyecto se trata de un juego de Ajedrez utilizando IA hecho por Python y como modulo principal
Pygame, este proyecto esta inspirado por Eddie Sharick y su contenido relacionado a esto. 
Este repositorio es el resultado de seguir su contenido y proponer algunas mejoras por mi cuenta
y actualizar a versiones mas recientes asi mismo usar una interfaz de menu propio y tener un codigo
mas limpio. Por la presente, te recomiendo que visites su canal de YouTube y mires su
contenido tambien te dejare mi github donde podras ver este repositorio muy pronto.

[Canal de YT Eddie's](https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww)

[Primer episodio de "Chess engine in Python"](https://www.youtube.com/watch?v=EnYui0e73Rs&ab_channel=EddieSharick)

[xMeiker - Github](https://github.com/xmeiker)

## Tecnologias
* Python 3.12
* pygame 2.5.2

## Cosas por implementar o mejoras
- [ ] Limpiar aun más el código: ahora mismo es realmente complicado.
- [ ] Usar matrices numerosas en lugar de listas 2D.
- [ ] Estancamiento en 3 movimientos repetidos o 50 movimientos sin captura/avance de peón.
- [ ] Menú para seleccionar jugador vs jugador/computadora.
- [ ] Permitir arrastrar piezas.
- [ ] Resolver movimientos ambiguos (notación).

## Instrucciones
1. Clona este repositorio.
2. Seleccione si desea jugar contra la computadora, contra otro jugador localmente o ver el juego del motor contra sí mismo configurando las banderas apropiadas en las líneas 52 y 53 de `ChessMain.py`.
3. Ejecutar `ChessMain.py`.
4. ¡Disfruta el juego!

#### Controles:
* Presionar `z` para deshacer un movimiento.
* Presionar `r` para reiniciar el juego.

## Otras ideas de desarrollo
1. Ordenar los movimientos (por ejemplo, mirar controles y/o capturas) debería hacer que el motor sea mucho más rápido (debido a la poda alfa-beta).
2. Realizar un seguimiento de todos los movimientos posibles en una posición determinada, de modo que después de realizar un movimiento, el motor no tenga que volver a calcular todos los movimientos.
3. Evaluar la ubicación de los reyes en el tablero (separados en el medio juego y al final del juego).
4. Libro de aperturas.
