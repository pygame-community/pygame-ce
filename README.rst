.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :width: 800
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

**English** `简体中文`_ `繁體中文`_ `Français`_ `فارسی`_ `Español`_ `日本語`_ `Italiano`_ `Русский`_
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Pygame_ is a free and open-source cross-platform library
for the development of multimedia applications like video games using Python.
It uses the `Simple DirectMedia Layer library`_ and several other
popular libraries to abstract the most common functions, making writing
these programs a more intuitive task.

This distribution is called **'pygame - Community Edition'** ('pygame-ce' for short).

It is a fork of the upstream pygame project by its former core developers,
and was created after impossible challenges prevented them from continuing development upstream.
The new distribution aims to offer more frequent releases, continuous bugfixes and enhancements,
and a more democratic governance model.

New contributors are welcome!


Installation
------------

::

   pip install pygame-ce


Help
----

If you are just getting started with pygame, you should be able to
get started fairly quickly.  Pygame comes with many tutorials and
introductions.  There is also full reference documentation for the
entire library. Browse the documentation on the `docs page`_. You
can also browse the documentation locally by running
``python -m pygame.docs`` in your terminal. If the docs aren't found
locally, it'll launch the online website instead.

The online documentation stays up to date with the development version
of pygame on github.  This may be a bit newer than the version of pygame
you are using. To upgrade to the latest full release, run
``pip install pygame-ce --upgrade`` in your terminal.

Best of all, the examples directory has many playable small programs
which can get you started playing with the code right away.


Building From Source
--------------------

If you want to use features that are currently in development,
or you want to contribute to pygame-ce, you will need to build pygame-ce
locally from its source code, rather than pip installing it.

Installing from source is fairly automated. The most work will
involve compiling and installing all the pygame dependencies.  Once
that is done, run the ``setup.py`` script which will attempt to
auto-configure, build, and install pygame.

Much more information about installing and compiling is available
on the `Compilation wiki page`_.


Credits
-------

Thanks to everyone who has helped contribute to this library.
Special thanks are also in order.

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

Thanks to those sending in patches and fixes: Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber,
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

And our bug hunters above and beyond: Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau

There's many more folks out there who've submitted helpful ideas, kept
this project going, and basically made our life easier.  Thanks!

Many thank you's for people making documentation comments, and adding to the
`pygame documentation`_ and the `pygame-ce documentation`_.

Also many thanks for people creating games and putting them on the
pygame.org website for others to learn from and enjoy.

Lots of thanks to James Paige for hosting the pygame bugzilla.

Also a big thanks to Roger Dingledine and the crew at SEUL.ORG for our
excellent hosting.

Dependencies
------------

Pygame is obviously strongly dependent on SDL and Python. It also
links to and embeds several other smaller libraries. The font
module relies on SDL_ttf, which is dependent on freetype. The mixer
(and mixer.music) modules depend on SDL_mixer. The image module
depends on SDL_image. Transform.rotozoom has an embedded version
of SDL_rotozoom, and gfxdraw has an embedded version of SDL_gfx.
Dependency versions:


+----------+------------------------+
| CPython  | >= 3.9 (Or use PyPy3)  |
+----------+------------------------+
| SDL      | >= 2.0.14              |
+----------+------------------------+
| SDL_mixer| >= 2.0.4               |
+----------+------------------------+
| SDL_image| >= 2.0.4               |
+----------+------------------------+
| SDL_ttf  | >= 2.0.15              |
+----------+------------------------+

How to Contribute
-----------------
First of all, thank you for considering contributing to pygame-ce! It's people like you that make pygame-ce a great library. Please follow these steps to get started:

1. Read the `Contribution Guidelines`_ and the `Many Ways to Contribute`_ wiki pages.
2. Read the documentataion on `Opening A Pull Request`_ and `Opening a Great Pull Request`_.
3. Read how to `label and link reported issues`_.
4. Check the `issue tracker`_ for open issues that interest you or open a new issue to start a discussion about your idea.

There are many more resources throughout the `wiki pages`_ that can help you get started.

If you have any questions, please feel free to ask in the `Pygame Community Discord Server`_ or open an issue.

License
-------
**License Identifier:** LGPL-2.1-or-later

This library is distributed under `GNU LGPL version 2.1`_, which can
be found in the file ``docs/LGPL.txt``.  We reserve the right to place
future versions of this library under a different license.

This basically means you can use pygame in any project you want,
but if you make any changes or additions to pygame itself, those
must be released with a compatible license (preferably submitted
back to the pygame-ce project).  Closed source and commercial games are fine.

The programs in the ``examples`` subdirectory are in the public domain.

See docs/licenses for licenses of dependencies.


.. |PyPiVersion| image:: https://img.shields.io/pypi/v/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |PyPiLicense| image:: https://img.shields.io/pypi/l/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |Python3| image:: https://img.shields.io/badge/python-3-blue.svg?v=1

.. |GithubCommits| image:: https://img.shields.io/github/commits-since/pygame-community/pygame-ce/2.5.2.svg
   :target: https://github.com/pygame-community/pygame-ce/compare/2.5.3...main

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

.. _简体中文: ./docs/readmes/README.zh-cn.rst
.. _繁體中文: ./docs/readmes/README.zh-tw.rst
.. _Français: ./docs/readmes/README.fr.rst
.. _فارسی: ./docs/readmes/README.fa.rst
.. _Español: ./docs/readmes/README.es.rst
.. _日本語: ./docs/readmes/README.ja.rst
.. _Italiano: ./docs/readmes/README.it.rst
.. _Русский: ./docs/readmes/README.ru.rst
