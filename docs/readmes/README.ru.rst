.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :width: 800
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ `简体中文`_ `繁體中文`_ `Français`_ `فارسی`_ `Español`_ `日本語`_ `Italiano`_ **Русский**
---------------------------------------------------------------------------------------------------

Pygame_  - бесплатная кроссплатформенная библиотека с открытым исходным кодом
для разработки мультимедийных приложений, таких как видеоигры, с использованием Python.
Он использует `Simple DirectMedia Layer library`_ и несколько других популярных библиотек
для абстрагирования наиболее распространенных функций,
что делает написание этих программ более интуитивно понятной задачей.


Этот дистрибутив называется **'pygame - Community Edition'** (сокращённо 'pygame-ce').

Это ответвление исходного проекта pygame от его бывших главных разработчиков и было создано после того, как непреодолимые
трудности помешали им продолжить разработку исходного проекта.
Новый дистрибутив призван предлагать более частые выпуски, постоянные исправления и усовершенствования,
а также более демократичную модель управления.

Новые участники приветствуются!


Установка
------------

::

   pip install pygame-ce


Справка
----

Если вы только начинаете работать с pygame, вы сможете приступить к работе довольно быстро.
Pygame поставляется с множеством руководств и введений.
Также имеется полная справочная документация по всей библиотеке.
Просмотрите документацию на страниц `docs page`_.
Вы также можете просмотреть документацию локально, запустив
``python -m pygame.docs`` в Вашем терминале. Если документы не найдены
локально, вместо этого будет запущен онлайн-сайт.

Интерактивная документация соответствует версии pygame для разработки на github.
Она может быть немного новее, чем версия pygame, которую вы используете.
Чтобы перейти на последнюю выпущенную версию, запустите
``pip install pygame-ce --upgrade`` в Вашем терминале.

Лучше всего то, что в каталоге examples есть множество воспроизводимых небольших программ,
которые помогут вам сразу начать работу с кодом.


Сборка из исходного кода
--------------------

Если вы хотите использовать функции, которые в настоящее время находятся в разработке,
или вы хотите внести свой вклад в pygame-ce,
вам нужно будет создать pygame-ce локально из его исходного кода, а не устанавливать его pip.

Установка из исходного кода довольно автоматизирована.
Основная работа будет включать компиляцию и установку всех зависимостей pygame.
Как только это будет сделано, запустите сценарий ``setup.py``,
который попытается автоматически настроить, собрать и установить pygame.

Гораздо больше информации об установке и компиляции доступно
на `Compilation wiki page`_.


Заслуги
-------

Спасибо всем, кто помог внести свой вклад в эту библиотеку.
Также уместна особая благодарность.

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

Спасибо тем, кто присылает патчи и исправления: Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber,
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

И наши охотники за багами выше всяких похвал: Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau

Есть еще много людей, которые предоставили полезные идеи,
поддержали этот проект и, по сути, упростили нам жизнь. Спасибо!

Большое спасибо людям, которые комментируют документацию и добавляют в
`pygame documentation`_ и `pygame-ce documentation`_.

Также большое спасибо за людей, создающих игры и размещающих их на веб-сайте
pygame.org, чтобы другие могли учиться и получать удовольствие.

Огромное спасибо James Paige за хостинг pygame bugzilla.

Также большое спасибо Roger Dingledine и команде SEUL.ORG за наш
отличный хостинг.


Зависимости
------------

Pygame, очевидно, сильно зависит от SDL и Python. Он также
ссылается на несколько других библиотек меньшего размера и встраивает их. Модуль font
использует SDL_ttf, который зависит от freetype. Модули mixer
(и mixer.music) зависят от SDL_mixer. Модуль image
зависит от SDL_image. Transform.rotozoom имеет встроенную версию
SDL_rotozoom, а gfxdraw имеет встроенную версию SDL_gfx.
Версии зависимостей:


+----------+------------------------+
| CPython  | >= 3.8 (Or use PyPy3)  |
+----------+------------------------+
| SDL      | >= 2.0.10              |
+----------+------------------------+
| SDL_mixer| >= 2.0.4               |
+----------+------------------------+
| SDL_image| >= 2.0.4               |
+----------+------------------------+
| SDL_ttf  | >= 2.0.15              |
+----------+------------------------+

Как внести свой вклад
-----------------
Прежде всего, спасибо, что согласились внести свой вклад в pygame-ce! Именно такие люди, как вы, делают pygame-ce отличной библиотекой. Пожалуйста, выполните следующие действия, чтобы начать:

1. Read the `Contribution Guidelines`_ and the `Many Ways to Contribute`_ wiki pages.
2. Read the documentataion on `Opening A Pull Request`_ and `Opening a Great Pull Request`_.
3. Read how to `label and link reported issues`_.
4. Check the `issue tracker`_ for open issues that interest you or open a new issue to start a discussion about your idea.

There are many more resources throughout the `wiki pages`_ that can help you get started.

If you have any questions, please feel free to ask in the `Pygame Community Discord Server`_ or open an issue.

License
-------
**License Identifier:** LGPL-2.1-or-later

Эта библиотека распространяется под лицензией `GNU LGPL version 2.1`_, которую можно
найти в файле ``docs/LGPL.txt``.  Мы оставляем за собой право размещать
будущие версии этой библиотеки под другой лицензией.

По сути, это означает, что вы можете использовать pygame в любом проекте, который захотите,
но если вы вносите какие-либо изменения или дополнения в саму pygame, они
должны быть выпущены с совместимой лицензией (preferably submitted
back to the pygame-ce project).  Игры с закрытым исходным кодом и коммерческие игры - это нормально.

Программы в подкаталоге ``examples`` находятся в открытом доступе.

Смотрите docs/licenses, чтобы узнать лицензии на зависимости.


.. |PyPiVersion| image:: https://img.shields.io/pypi/v/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |PyPiLicense| image:: https://img.shields.io/pypi/l/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |Python3| image:: https://img.shields.io/badge/python-3-blue.svg?v=1

.. |GithubCommits| image:: https://img.shields.io/github/commits-since/pygame-community/pygame-ce/2.4.1.svg
   :target: https://github.com/pygame-community/pygame-ce/compare/2.4.1...main

.. |DocsStatus| image:: https://img.shields.io/website?down_message=offline&label=docs&up_message=online&url=https%3A%2F%2Fpyga.me%2Fdocs%2F
   :target: https://pyga.me/docs/

.. |BlackFormatBadge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. _Pygame: https://pyga.me
.. _pygame-ce documentation: https://pyga.me/docs/
.. _pygame documentation: https://www.pygame.org/docs/
.. _Simple DirectMedia Layer library: https://www.libsdl.org
.. _Compilation wiki page: https://github.com/pygame-community/pygame-ce/wiki#compiling
.. _docs page: https://pyga.me/docs
.. _GNU LGPL version 2.1: https://www.gnu.org/copyleft/lesser.html
.. _Contribution Guidelines: https://github.com/pygame-community/pygame-ce/wiki/Contribution-guidelines
.. _Many Ways to Contribute: https://github.com/pygame-community/pygame-ce/wiki/Many-ways-to-contribute
.. _Opening A Pull Request: https://github.com/pygame-community/pygame-ce/wiki/Opening-a-pull-request
.. _Opening a Great Pull Request: https://github.com/pygame-community/pygame-ce/wiki/Opening-a-great-pull-request
.. _issue tracker: https://github.com/pygame-community/pygame-ce/issues
.. _label and link reported issues: https://github.com/pygame-community/pygame-ce/wiki/Labelling-&-linking-reported-issues
.. _Pygame Community Discord Server: https://discord.gg/pygame
.. _wiki pages: https://github.com/pygame-community/pygame-ce/wiki

.. _English: ./../../README.rst
.. _简体中文: README.zh-cn.rst
.. _繁體中文: README.zh-tw.rst
.. _Français: README.fr.rst
.. _فارسی: README.fa.rst
.. _Español: README.es.rst
.. _日本語: README.ja.rst
.. _Italiano: README.it.rst
