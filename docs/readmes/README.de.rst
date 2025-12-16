.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
   :width: 800
   :alt: pygame
   :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

**Deutsch** `简体中文`_ `繁體中文`_ `Français`_ `فارسی`_ `Español`_ `日本語`_ `Italiano`_ `Русский`_ `Ελληνικά`_ `Português (Brasil)`_
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Pygame_ ist eine freie und quelloffene, plattformübergreifende Bibliothek
zur Entwicklung von Multimedia-Anwendungen wie Videospielen mit Python.
Sie verwendet die `Simple DirectMedia Layer library`_ sowie mehrere andere
beliebte Bibliotheken, um die gängigsten Funktionen zu abstrahieren und
das Schreiben solcher Programme intuitiver zu machen.

Diese Distribution heißt **„pygame – Community Edition“** (kurz „pygame-ce“).

Sie ist ein Fork des ursprünglichen pygame-Projekts durch dessen frühere Kernentwickler
und wurde geschaffen, nachdem unüberwindbare Herausforderungen eine Weiterentwicklung
im Upstream-Projekt verhinderten.
Die neue Distribution verfolgt das Ziel, häufigere Releases, kontinuierliche Fehlerbehebungen
und Verbesserungen sowie ein demokratischeres Governance-Modell anzubieten.

Neue Mitwirkende sind herzlich willkommen!


Installation
------------

Um pygame-ce zu installieren, stellen Sie zunächst sicher, dass Python (und pip)
installiert und über Ihren PATH verfügbar sind.
Führen Sie anschließend folgenden Befehl in Ihrem Terminal oder in der Eingabeaufforderung aus:

::

   pip install pygame-ce

Beachten Sie, dass Sie auf manchen Plattformen möglicherweise ``pip3`` anstelle von ``pip`` verwenden müssen.

Linux-Hinweis: Fehler „Breaking System Packages“
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Auf einigen Linux-Distributionen (wie Ubuntu oder Debian) kann das Installieren
von Python-Paketen mit ``pip`` eine Meldung wie die folgende auslösen:

::

   error: externally-managed-environment
   This environment is externally managed when system packages are installed.

Das bedeutet, dass das System-Python vom Betriebssystem verwaltet wird und eine
globale Verwendung von ``pip3`` mit Systempaketen kollidieren könnte.

Empfohlene Lösungen
^^^^^^^^^^^^^^^^^^^

1. Verwendung von ``venv`` (Virtuelle Umgebung):

   Sie können eine virtuelle Umgebung erstellen und pygame-ce darin installieren.
   So nutzen Sie weiterhin das System-Python, erstellen aber eine separate Umgebung
   für installierte Pakete, sodass diese keine Systempakete beeinträchtigen.

   .. code-block:: bash

      python3 -m venv venv      # erstellt eine venv mit dem Namen „venv“
      source venv/bin/activate  # aktiviert die venv
      pip install pygame-ce     # installiert Pakete in der venv

2. Verwendung von ``pyenv`` (Python-Verwaltung auf Benutzerebene):

   `pyenv <https://github.com/pyenv/pyenv>`_ ermöglicht es Ihnen, eigene Python-Versionen
   auf Benutzerebene zu installieren und zu verwalten, ohne das System-Python anzutasten.
   Zusätzlich können mehrere Python-Versionen parallel genutzt werden.

3. Verwendung von ``uv`` (schneller moderner Paketinstaller):

   `uv <https://docs.astral.sh/uv/>`_ ist ein moderner, schneller Paket- und Umgebungsmanager
   für Python und kann als Ersatz für ``venv`` und ``pyenv`` dienen.

Hilfe
-----

Wenn Sie gerade erst mit pygame beginnen, sollten Sie relativ schnell einsteigen können.
Pygame bringt viele Tutorials und Einführungen mit. Außerdem gibt es eine vollständige
Referenzdokumentation für die gesamte Bibliothek.
Durchsuchen Sie die Dokumentation auf der `Docs-Seite`_.
Sie können die Dokumentation auch lokal aufrufen, indem Sie im Terminal
``python -m pygame.docs`` ausführen. Wenn die Dokumentation lokal nicht gefunden wird,
öffnet sich stattdessen die Online-Webseite.

Die Online-Dokumentation wird stets mit der Entwicklungsversion von pygame auf GitHub
aktualisiert und kann daher etwas neuer sein als die von Ihnen verwendete Version.
Um auf die neueste stabile Version zu aktualisieren, führen Sie
``pip install pygame-ce --upgrade`` im Terminal aus.

Besonders hilfreich ist auch das ``examples``-Verzeichnis, das viele spielbare
kleine Programme enthält, mit denen Sie sofort mit dem Code experimentieren können.


Kompilieren aus dem Quellcode
----------------------------

Wenn Sie Funktionen nutzen möchten, die sich aktuell in Entwicklung befinden,
oder wenn Sie zu pygame-ce beitragen möchten, müssen Sie pygame-ce lokal aus dem
Quellcode bauen, anstatt es per pip zu installieren.

Die Installation aus dem Quellcode ist weitgehend automatisiert.
Der größte Aufwand besteht im Kompilieren und Installieren aller pygame-Abhängigkeiten.
Sobald dies erledigt ist, führen Sie das Skript ``setup.py`` aus, das versucht,
pygame automatisch zu konfigurieren, zu bauen und zu installieren.

Weitere Informationen zum Installieren und Kompilieren finden Sie auf der
`Compilation wiki page`_.


Danksagungen
------------

Vielen Dank an alle, die zur Entwicklung dieser Bibliothek beigetragen haben.
Ein besonderer Dank gilt:

* Marcus Von Appen: zahlreiche Änderungen und Fehlerbehebungen, FreeBSD-Maintainer ab 1.7.1+
* Lenard Lindstrom: Windows-Maintainer ab 1.8+, viele Änderungen und Fixes
* Brian Fisher für den SVN-Autobuilder, Bugtracker und viele Beiträge
* Rene Dudfield: zahlreiche Änderungen und Fixes, Release-Manager/Maintainer ab 1.7+
* Phil Hassey für seine Arbeit an der pygame.org-Webseite
* DR0ID für seine Arbeit am Sprite-Modul
* Richard Goedeken für die smoothscale-Funktion
* Ulf Ekström für den pixelgenauen Kollisionscode
* Pete Shinners: ursprünglicher Autor
* David Clark für die Rolle als „rechte Hand“
* Ed Boraas und Francis Irving: Debian-Pakete
* Maxim Sobolev: FreeBSD-Paketierung
* Bob Ippolito: macOS- und OS-X-Portierung (sehr viel Arbeit!)
* Jan Ekhol, Ray Kelm und Peter Nicolai: Geduld mit frühen Designideen
* Nat Pryce für den Start der Unit-Tests
* Dan Richter für Dokumentationsarbeit
* TheCorruptor für die beeindruckenden Logos und Grafiken
* Nicholas Dudfield: zahlreiche Testverbesserungen
* Alex Folkner für pygame-ctypes

Dank auch an alle, die Patches und Fixes eingesendet haben: Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber,
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

Und ein besonderer Dank an unsere außergewöhnlichen Bugfinder: Angus,
Guillaume Proux, Frank Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama,
Mike Mulcheck, Michael Benfield, David Lau.

Es gibt noch viele weitere Personen, die hilfreiche Ideen eingebracht,
das Projekt am Laufen gehalten und uns die Arbeit erleichtert haben.
Vielen Dank!

Vielen Dank auch an alle, die Dokumentationskommentare geschrieben und zur
`pygame documentation`_ sowie zur `pygame-ce documentation`_ beigetragen haben.

Ebenso vielen Dank an alle, die Spiele erstellt und auf der pygame.org-Webseite
veröffentlicht haben, damit andere daraus lernen und Freude daran haben können.

Großer Dank an James Paige für das Hosting von Bugzilla.

Ein weiterer großer Dank geht an Roger Dingledine und das Team von SEUL.ORG
für das hervorragende Hosting.


Abhängigkeiten
--------------

Pygame ist selbstverständlich stark von SDL und Python abhängig.
Zusätzlich bindet es mehrere kleinere Bibliotheken ein.
Das Font-Modul basiert auf SDL_ttf, welches von freetype abhängt.
Die Module mixer (und mixer.music) hängen von SDL_mixer ab.
Das Image-Modul verwendet SDL_image.
Transform.rotozoom enthält eine eingebettete Version von SDL_rotozoom,
und gfxdraw eine eingebettete Version von SDL_gfx.
Abhängigkeitsversionen:

+-----------+--------------------------+
| CPython   | >= 3.10 (oder PyPy3)     |
+-----------+--------------------------+
| SDL       | >= 2.0.14                |
+-----------+--------------------------+
| SDL_mixer | >= 2.0.4                 |
+-----------+--------------------------+
| SDL_image | >= 2.0.4                 |
+-----------+--------------------------+
| SDL_ttf   | >= 2.0.15                |
+-----------+--------------------------+


Mitwirken
---------

Zunächst einmal vielen Dank, dass Sie in Erwägung ziehen, zu pygame-ce beizutragen!
Menschen wie Sie machen pygame-ce zu einer großartigen Bibliothek.
Bitte folgen Sie diesen Schritten für den Einstieg:

1. Lesen Sie die `Contribution Guidelines`_ und die Wiki-Seite `Many Ways to Contribute`_.
2. Lesen Sie die Dokumentation zu `Opening A Pull Request`_ und `Opening a Great Pull Request`_.
3. Informieren Sie sich darüber, wie gemeldete Issues `label and link reported issues`_ korrekt werden.
4. Prüfen Sie den `issue tracker`_ auf offene Issues, die Sie interessieren, oder eröffnen Sie ein neues Issue, um eine Diskussion zu starten.

Weitere hilfreiche Ressourcen finden Sie auf den verschiedenen `wiki pages`_.

Bei Fragen können Sie sich gerne im `Pygame Community Discord Server`_ melden
oder ein Issue eröffnen.


Lizenz
------

**Lizenzkennung:** LGPL-2.1-or-later

Diese Bibliothek wird unter der `GNU LGPL version 2.1`_ veröffentlicht,
die in der Datei ``docs/LGPL.txt`` zu finden ist.
Wir behalten uns das Recht vor, zukünftige Versionen dieser Bibliothek
unter einer anderen Lizenz zu veröffentlichen.

Das bedeutet im Wesentlichen, dass Sie pygame in jedem beliebigen Projekt
verwenden dürfen. Wenn Sie jedoch Änderungen oder Erweiterungen an pygame selbst
vornehmen, müssen diese unter einer kompatiblen Lizenz veröffentlicht werden
(vorzugsweise zurück an das pygame-ce-Projekt).
Closed-Source- und kommerzielle Spiele sind erlaubt.

Die Programme im Unterverzeichnis ``examples`` sind gemeinfrei (Public Domain).

Siehe docs/licenses für die Lizenzen der Abhängigkeiten.


.. |PyPiVersion| image:: https://img.shields.io/pypi/v/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |PyPiLicense| image:: https://img.shields.io/pypi/l/pygame-ce.svg?v=1
   :target: https://pypi.python.org/pypi/pygame-ce

.. |Python3| image:: https://img.shields.io/badge/python-3-blue.svg?v=1

.. |GithubCommits| image:: https://img.shields.io/github/commits-since/pygame-community/pygame-ce/2.5.6.svg
   :target: https://github.com/pygame-community/pygame-ce/compare/2.5.6...main

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
.. _Ελληνικά: ./docs/readmes/README.gr.rst
.. _Português (Brasil): ./docs/readmes/README.pt-br.rst
