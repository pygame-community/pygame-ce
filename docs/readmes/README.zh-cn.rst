.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ **简体中文** `繁體中文`_ `Français`_ `فارسی`_ `Español`_ `日本語`_ `Italiano`_ `Русский`_

----

Pygame_ 是一款自由且开源的跨平台库，用于开发电子游戏等多媒体应用。Pygame基于 `Simple DirectMedia Layer library`_ 以及其他几个广受欢迎的库，汲取其中最常见的函数，让编写游戏成为更加符合直觉的事情。

本发行版名为 **“pygame - Community Edition”** （简称 “pygame-ce”）。

pygame-ce是上游pygame项目的分支，由此前pygame项目的核心开发者创建。开发者们在上游的开发中受到了强烈的阻挠，无法继续，所以创建了这个发行版。新的发行版旨在提供更加频繁的版本更新，持续不断的bug修复与功能增强，以及更加民主的管理模式。

欢迎新的贡献者加入我们。

安装
------------

::

   pip install pygame-ce


入门
----

刚接触pygame的初学者应该可以快速入门。pygame提供了大量教程与介绍，也提供了整个库的完整参考文档。你可以在 `docs page`_ 浏览文档。也可以在终端中运行`python -m pygame.docs`，在本地浏览文档。如果找不到本地文档，会自动打开在线文档。

在线文档与github中的开发版pygame同步。文档版本可能比你正在用的pygame版本新一些。在终端中运行 ``pip install pygame-ce --upgrade`` 可以升级到最新完整版本。

最重要的是，examples目录中有许多可以玩的小程序，可以使你立即开启代码之旅。

从源码开始编译
--------------------

如果你想使用那些正在开发的特性，或者你想要为pygame做出贡献，你就需要从源码开始编译pygame，而不是用pip进行安装。

编译与安装的流程是高度自动化的。你要做的工作主要是pygame依赖的编译与安装。一旦完成，你就可以运行`setup.py`，它会尝试完成自动配置，编译，然后安装pygame。

更多关于编译与安装信息，参见 `Compilation wiki page`_ 。

鸣谢
-------

感谢为本库做成贡献的每一个人。

特别鸣谢：

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

感谢发送补丁/修复的人：Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber,
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

以及我们卓越的bug猎人：Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau

还有许多人提交了有用的想法，助力本项目前进，使我们的生活变得更加轻松。感谢你们！

感谢对文档做成评论并将其添加到pygame.org wiki的人。

感谢制作游戏并把游戏放到pygame.org网站供人学习与娱乐的人。

感谢 James Paige 建立了pygame bugzilla。

感谢 Roger Dingledine 与SEUL.ORG上的crew，感谢我们优秀的主持。

依赖
------------
pygame显然依赖于SDL和Python。此外pygame还嵌入了几个较小的库：font模块依赖于SDL_ttf（SDL_ttf依赖于freetype）；mixer模块（以及mixer.music模块）依赖于SDL_mixer；image模块依赖于SDL_image；transform模块内嵌了一个SDL_rotozoom来实现rotozoom函数；gfxdraw模块内嵌了一个SDL_gfx。

依赖的版本要求如下：


+----------+------------------------+
| CPython  | >= 3.9 （或 PyPy3）    |
+----------+------------------------+
| SDL      | >= 2.0.14              |
+----------+------------------------+
| SDL_mixer| >= 2.0.4               |
+----------+------------------------+
| SDL_image| >= 2.0.4               |
+----------+------------------------+
| SDL_ttf  | >= 2.0.15              |
+----------+------------------------+



许可证
-------
**许可证标识符:** LGPL-2.1-or-later

本库在 `GNU LGPL version 2.1`_ 下发布，许可文件： ``docs/LGPL.txt`` 。我们保留将此库的未来版本置于其他许可证下的权利。

这基本代表着你可以在任意项目中使用pygame，但如果你修改或者增加了pygame库的内容，这些内容必须使用兼容的许可证发布（更可取的是将其提交回pygame项目）。闭源或者商业性游戏中可以使用pygame。

``examples`` 目录中的程序不受版权限制。

有关依赖项的许可证，请参阅 ``docs/licenses`` 。



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

.. _pygame: https://www.pyga.me
.. _Simple DirectMedia Layer library: https://www.libsdl.org
.. _Compilation wiki page: https://github.com/pygame-community/pygame-ce/wiki#compiling
.. _docs page: https://pyga.me/docs
.. _GNU LGPL version 2.1: https://www.gnu.org/copyleft/lesser.html

.. _English: ./../../README.rst
.. _繁體中文: README.zh-tw.rst
.. _Français: README.fr.rst
.. _فارسی: README.fa.rst
.. _Español: README.es.rst
.. _日本語: README.ja.rst
.. _Italiano: README.it.rst
.. _Русский: README.ru.rst
