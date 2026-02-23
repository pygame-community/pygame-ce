.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :width: 800
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ `简体中文`_ `繁體中文`_ `Français`_ `فارسی`_ `Español`_ `日本語`_ **Italiano** `Русский`_ `Ελληνικά`_ `Português (Brasil)`_ `Deutsch`_
---------------------------------------------------------------------------------------------------

Pygame_ è una libreria open source gratuita e multipiattaforma
adibita allo sviluppo di applicazioni multimediali come videogiochi utilizzando Python.
Utilizza la `Simple DirectMedia Layer library`_ e altre librerie
popolari per astrarre le operazioni più comuni, rendendo la scrittura
di questi programmi un compito più intuitivo.

Questa distribuzione si chiama **`pygame - Community Edition`** ('pygame-ce' per abbreviare).

È una fork (divisione) del progetto pygame originale fondata dai suoi precedenti sviluppatori principali,
ed è stata creata dopo che ostacoli insuperabili gli hanno impedito di continuare a sviluppare l'originale.
La nuova distribuzione ha l'obbiettivo di offrire nuove versioni più di frequente, continue migliorie
e bugfixes e un modello governativo più democratico.

Nuovi contributori sono i benvenuti!

Installazione
-------------

::

   pip install pygame-ce


Aiuto
-----

Se sei alle prime armi con pygame, dovresti riuscire a iniziare
abbastanza velocemente. Pygame ha a disposizione numerosi tutorial
e introduzioni. Esiste anche una documentazione di riferimento completa
per l'intera libreria. Puoi trovare la documentazione sulla `docs page`_.
Puoi anche visualizzare la documentazione localmente eseguento il comando
``python -m pygame.docs`` nel tuo terminale. Se la documentazione è
inaccessibile localmente, il sito web online verrà aperto al suo posto.

La documentazione online è aggiornata con la versione di sviluppo di pygame-ce
su github. Essa potrebbe essere leggermente più recente rispetto alla versione
di pygame-ce che stai usando. Per aggiornare alla versione più recente, esegui
il comando ``pip install pygame-ce --upgrade`` nel tuo terminale.

La cosa migliore è che la cartella degli esempi contiene numerosi piccoli
programmi giocabili che ti permetteranno di iniziare a maneggiare il codice
fin da subito.

Compilare dal Codice Locale
---------------------------

Se vuoi usare funzionalità che sono ancora in sviluppo o se vuoi
contribuire per pygame-ce avrai bisogno di compilare pygame-ce localmente
a partire dal suo codice sorgente piuttosto che installarlo con pip.

L'installazione dal codice sorgente è abbastanza automatizzata. La maggior
parte del lavoro riguarda compilare e installare le librerie richieste da pygame-ce.
Fatto ciò, esegui lo script ``setup.py`` che tenterà di
configurare automaticamente, compilare e installare pygame-ce.

Più informazioni riguardo all'installazione e alla compilazione sono
disponibili sulla `Compilation wiki page`_.

Requisiti
---------

Pygame come si può intuire dipende fortemente da SDL e da Python.
È inoltre collegata e incorpora diverse altre librerie più piccole.
Il modulo font dipende da SDL_ttf che dipende a sua volta da freetype.
Il modulo mixer (e mixer.music) dipendono da SDL_mixer. Il modulo image
dipende da SDL_image. La funzione Transform.rotozoom usa una versione
incorporata di SDL_rotozoom e il modulo gfxdraw incorpora una versione
di SDL_gfx.

Le versioni dei requisiti:


+----------+------------------------+
| CPython  | >= 3.10 (Or use PyPy3) |
+----------+------------------------+
| SDL      | >= 2.0.14              |
+----------+------------------------+
| SDL_mixer| >= 2.0.4               |
+----------+------------------------+
| SDL_image| >= 2.0.4               |
+----------+------------------------+
| SDL_ttf  | >= 2.0.15              |
+----------+------------------------+

Come Contribuire
----------------
Prima di tutto, grazie per aver considerato di contribuire per pygame-ce! Sono le persone come te che rendono pygame-ce una libreria grandiosa. Per favore segui questi passaggi per iniziare:

1. Leggi le pagine wiki `Contribution Guidelines`_ e `Many Ways to Contribute`_.
2. Leggi la documentazione riguardo `Opening A Pull Request`_ e `Opening a Great Pull Request`_.
3. Leggi come `label and link reported issues`_.
4. Controlla l'`issue tracker`_ per problemi irrisolti che ti interessano o segnala un nuovo problema per iniziare una discussione riguardo alla tua idea.

Ci sono molte più risorse nelle `wiki pages`_ che possono aiutarti ad iniziare.

Se hai qualsiasi domanda, sentiti libero di chiedere nel `Pygame Community Discord Server`_ o segnala un problema.

Licenza
-------
**License Identifier:** LGPL-2.1-or-later

Questa libreria è distribuita con la licenza `GNU LGPL version 2.1`_ che può
essere trovata nel file ``docs/LGPL.txt``. Ci riserviamo il diritto di
distribuire future versioni di questa libreria con una licenza differente.

Questo significa essenzialmente che puoi usare pygame-ce in qualsiasi progetto
che tu voglia, ma se fai alcun cambiamento o aggiunte a pygame-ce stesso,
tali modifiche devono essere distribuite con una licenza compatibile (preferibilmente
presentate al progetto pygame-ce). Giochi commerciali o a codice chiuso sono consentiti.

I programmi nella sottocartella ``examples`` appartengono al dominio pubblico.

Controlla docs/licenses per le licenze dei requisiti.

****

**Last reviewed**: 05 October 2024 - **Ultima revisione**: 05 Ottobre 2024

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
.. _فارسی: README.fa.rst
.. _Français: README.fr.rst
.. _Español: README.es.rst
.. _日本語: README.ja.rst
.. _Italiano: README.it.rst
.. _Русский: README.ru.rst
.. _Ελληνικά: README.gr.rst
.. _Português (Brasil): README.pt-br.rst
.. _Deutsch: README.de.rst
