.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ `简体中文`_ `繁體中文`_ `Français`_ `فارسی`_ **Español** `日本語`_ `Italiano`_ `Русский`_

---------------------------------------------------------------------------------------------------------------------------------------------------

`Pygame`_ es una biblioteca multiplataforma, gratuita y de código abierto
permitiéndole desarrollar aplicaciones multimedia como videojuegos, con Python.
Utiliza la biblioteca « `Simple DirectMedia Layer`_ » (SDL) y varias otras bibliotecas
popular para abstraer las funciones más comunes y hace  la escritura de programas
lo más intuitivo posible.

Esta distribución se llama **« pygame - Community Edition »** (abreviado « pygame-ce »).


Esta es una bifurcación del proyecto original de sus principales desarrolladores anteriores. Fue creado como resultado de muchos obstáculos que eran imposibles de superar, impidiéndoles continuar el desarrollo del proyecto inicial. Esta nueva distribución tiene como objetivo ofrecer actualizaciones más regular, mejoras y correcciones, pero también un modelo de gobernanza más democrático.

¡Cualquier nuevo colaborador es bienvenido!

Instalacion
-----------

::

   pip install pygame-ce


Ayuda
-----

Si recién estás comenzando con pygame, deberías poder comenzar con él bastante rápidamente. Pygame viene con una gran cantidad de tutoriales e introducciones. Tienes también una documentación muy bien referenciada sobre toda la biblioteca. Navegas por el
documentación en `docs page`_. También puedes echarle un vistazo localmente por ejecución del comando ``python -m pygame.docs`` en tu terminal. Si la documentación
no se encuentra localmente, esto lanzará el sitio web.


La documentación en línea permanece actualizada con la versión actual de pygame-ce
desarrollo en GitHub. Esto puede ser un poco más nuevo que la versión de pygame-ce que usas. Para actualizar a la última versión publicada, ejecuta ``pip install pygame-ce --upgrade`` en tu terminal.

Un punto particularmente interesante: tienes a tu disposición un archivo de ejemplos que contienen muchos pequeños programas jugables, lo que le permite
para empezar a jugar con el código de inmediato.

Construir a partir del código fuente
------------------------------------

Si deseas utilizar características en desarrollo, o quieres contribuir a pygame-ce, vas a necesitar construir pygame-ce localmente a partir del código fuente, en lugar de instalarlo con pip.

La instalación de pygame-ce desde el código fuente está bastante automatizada. La mayor parte del trabajo consistirá en compilar e instalar todas las dependencias de
pygame-ce. Una vez hecho esto, ejecute el script ``setup.py`` que intentará autoconfigurar, compilar e instalación.

Más información sobre la instalación y compilación está disponible en `La pagina wiki de compilando`_.

Créditos
--------

Muchas gracias a todos los que han contribuido y siguen contribuyendo a este módulo.
Un agradecimiento especial también está en orden.

* Marcus Von Appen: many changes, and fixes, 1.7.1+ freebsd maintainer
* Lenard Lindstrom: the 1.8+ windows maintainer, many changes, and fixes
* Brian Fisher for svn auto builder, bug tracker and many contributions
* Rene Dudfield: many changes, and fixes, 1.7+ release manager/maintainer
* Phil Hassey for his work on the pygame.org website
* DR0ID for his work on the sprite module
* Richard Goedeken for his smoothscale function
* Ulf Ekström for his pixel perfect collision detection code
* Pete Shinners: original author
* David Clark for filling the right-hand-man position
* Ed Boraas and Francis Irving: Debian packages
* Maxim Sobolev: FreeBSD packaging
* Bob Ippolito: macOS and OS X porting (much work!)
* Jan Ekhol, Ray Kelm, and Peter Nicolai: putting up with early design ideas
* Nat Pryce for starting our unit tests
* Dan Richter for documentation work
* TheCorruptor for his incredible logos and graphics
* Nicholas Dudfield: many test improvements
* Alex Folkner for pygame-ctypes

Gracias a los que propusieron correcciones: Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber,
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

Y a nuestros cazadores de bugs: Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau

Hay muchas más personas por ahí que han presentado ideas útiles, han mantenido este proyecto en marcha y, básicamente, nos han hecho la vida más fácil. ¡Gracias!

Muchas gracias por las personas que hacen comentarios de documentación y agregan a `documentacion de pygame-ce`_.

Muchas gracias a James Paige en particular por ser anfitrión
pygame bugzilla.

También un gran agradecimiento a Roger Dingledine y la tripulación de SEUL.ORG por nuestro excelente alojamiento.

Dépendances
------------

**note:** This section translation is out of date (September 2023)

Pygame obviamente depende en gran medida de SDL y Python. También enlaza e incorpora varias otras bibliotecas más pequeñas. El módulo de fuentes se basa en SDL_ttf, que depende de freetype. Los módulos mixer (y mixer.music) dependen de SDL_mixer. El módulo de imagen depende de SDL_image, que también puede usar libjpeg y libpng. El módulo de transformación tiene una versión integrada de SDL_rotozoom para su propia función rotozoom.
El módulo surfarray necesita el paquete python numpy, para sus matrices numéricas multidimensionales.

Versiones de dependencia:

+----------+-----------------------------+
| CPython  | >= 3.9 (Ou utiliser PyPy3)  |
+----------+-----------------------------+
| SDL      | >= 2.0.14                   |
+----------+-----------------------------+
| SDL_mixer| >= 2.0.4                    |
+----------+-----------------------------+
| SDL_image| >= 2.0.4                    |
+----------+-----------------------------+
| SDL_ttf  | >= 2.0.15                   |
+----------+-----------------------------+

Licencia
--------
**Identificador de licencia:** LGPL-2.1-or-later

La biblioteca se distribuye bajo la licencia `GNU LGPL version 2.1`_, que se puede encontrar en el archivo ``docs/LGPL.txt``. Nos reservamos el derecho de licenciar versiones futuras de esta biblioteca bajo una licencia diferente.

Esto significa que tienes derecho a usar pygame-ce en cualquier proyecto que desee, pero solo si deseas realizar cambios o adiciones a Pygame-ce en sí, entonces estarás obligado publicarlos con una licencia compatible (preferiblemente enviándolos al proyecto pygame-ce). Se permiten códigos propietarios y juegos comerciales.

Los programas que se encuentran en el subdirectorio ``examples`` pertenecen a el dominio público.

Consulta docs/licenses para ver las licencias de dependencia.


.. |PyPiVersion| image:: https://img.shields.io/pypi/v/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |PyPiLicense| image:: https://img.shields.io/pypi/l/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |Python3| image:: https://img.shields.io/badge/python-3-blue.svg?v=1

.. |GithubCommits| image:: https://img.shields.io/github/commits-since/pygame-community/pygame-ce/2.3.0.svg
   :target: https://github.com/pygame-community/pygame-ce/compare/2.3.0...main

.. |DocsStatus| image:: https://img.shields.io/website?down_message=offline&label=docs&up_message=online&url=https%3A%2F%2Fpyga.me%2Fdocs%2F
   :target: https://pyga.me/docs/

.. |BlackFormatBadge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. _Pygame: https://www.pyga.me/
.. _documentacion de pygame-ce: https://pyga.me/docs/
.. _Simple DirectMedia Layer: https://www.libsdl.org
.. _La pagina wiki de compilando: https://github.com/pygame-community/pygame-ce/wiki#compiling
.. _docs page: https://pyga.me/docs
.. _GNU LGPL version 2.1: https://www.gnu.org/copyleft/lesser.html

.. _简体中文: README.zh-cn.rst
.. _繁體中文: README.zh-tw.rst
.. _English: ./../../README.rst
.. _فارسی: README.fa.rst
.. _Français: README.fr.rst
.. _日本語: README.ja.rst
.. _Italiano: README.it.rst
.. _Русский: README.ru.rst
