.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_logo.svg
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus| 
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ `简体中文`_ **Français**  `فارسی`_
---------------------------------------------------------------------------------------------------

Pygame est une bibliothèque multi-plateforme, libre et open-source
permettant de développer des applications multimédias comme des jeux-vidéos, avec Python.
Il utilise la bibliiothèque « `Simple DirectMedia Layer`_ » (SDL) et plusieurs autres bibliothèque
populaires pour abstraire les fonctions les plus courantes et rendre l’écriture de programmes
le plus intuitive possible.

Cette distribution se nomme **« pygame - Community Edition »** (abrégé « pygame-ce »).

Ceci est un fork du projet initial par ses principaux anciens développeurs,
il a été créé à cause de plusieurs obstacles impossibles à franchir, les empêchant de continuer
le développement du projet initial. Cette nouvelle distribution a pour but d’offrir des mises à jour
plus régulières, des améliorations et des correctifs, mais aussi un modèle de gouvernance plus
démocratique. 

Tout nouveau contributeur est le bienvenu ! 

Installation
------------

::

   pip install pygame-ce


Aide
----

Si vous venez de commencer avec pygame, vous devriez être capable de vous y lancer assez
rapidement. Pygame vient avec un grand nombre de tutoriels et d'introductions. Il y a
aussi une documentation très bien référencée sur toute la bibliothèque. Naviguez dans la
documentation sur la `docs page`_. Vous pouvez aussi y jeter un coup d'œil localement en
exécutant la commande ``python -m pygame.docs`` dans votre terminal. Si la documentation
n’est pas trouvée localement, cela va lancer le site web.

La documentation en ligne reste à jour avec la version de pygame-ce en cours de
développement sur GitHub. Cela peut être un peu plus récent que la version de
pygame que vous utilisez. Pour passer à la version sortie la plus récente, lancez
``pip install pygame-ce --upgrade`` dans votre terminal.

Un point particulièrement intéressant : vous avez à votre disposition un dossier 
d’exemples contenant beaucoup de petits programmes jouables, vous permettant
de commencer à jouer avec le code tout de suite.

Build depuis le code source
--------------------

Si vous voulez utiliser des fonctionnalités en cours de développement,
ou que vous voulez contribuer à pygame, vous allez avoir besoin de
build pygame localement depuis le code source, plutôt que de l’installer avec
pip.

Installer Pygame depuis le code source est assez automatisé. La majeure
partie du travail sera de compiler et d’installer toutes les dépendances de 
pygame. Une fois ceci fait, lancez le script ``setup.py`` qui va essayer 
de l’auto-configurer, le build, et l’installer.

Plus d’informations à propos de l’installation et de la compilation sont disponibles
sur `Compilation wiki page`_.

Crédits
-------

Un très grand merci à toutes celles et ceux qui ont contribué et contribuent
toujours à ce module.
Des remerciements particuliers s'imposent également.

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
* Bob Ippolito: MacOS and OS X porting (much work!)
* Jan Ekhol, Ray Kelm, and Peter Nicolai: putting up with early design ideas
* Nat Pryce for starting our unit tests
* Dan Richter for documentation work
* TheCorruptor for his incredible logos and graphics
* Nicholas Dudfield: many test improvements
* Alex Folkner for pygame-ctypes

Merci à celles et ceux qui ont proposé des correctifs : Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

Et à nos chasseurs de bugs : Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau

Il y a aussi pas mal de personnes présentes qui soumettent des idées utiles et intéressantes,
qui ont permis à ce projet de continuer à vivre, et qui ont pratiquement rendu notre
travail facile. Merci !

Très grands remerciements à toutes les personnes commentant la documentation,
et ajoutant du nouveau contenu dans le wiki pygame.org.  

Aussi de très grands remerciements à toutes les personnes créant des jeux et les 
partageant sur le site pygame.org pour permettre aux autres d'apprendre et de
s’amuser.

Très grands remerciements à James Paige en particulier pour avoir hébergé
pygame bugzilla.

Enfin nos meilleurs remerciements à Roger Dingledine et à toute l'équipe
de SEUL.ORG pour notre excellent hébergement.

Dépendances
------------

Pygame est évidemment très dépendant de SDL et Python. Il a aussi
des liens, mais de même intègre plusieurs autres petites bibliothèques.
Le module font s’appuie sur SDL_ttf, qui est lui-même dépendant de freetype.
Le module mixer (et mixer.music) dépend de SDL_mixer. Le module image
dépend de SDL_image, qui dépend de libjpeg et libpng. Le module transform
a une version intégrée de SDL_rotozoom pour ses propres fonctions de rotozoom.
Le module surfarray a besoin du package python, numpy, pour ses tableaux numériques
multidimensionnels.

Versions des dépendances:


+----------+------------------------+
| CPython  | >= 3.7 (Or use PyPy3)  |
+----------+------------------------+
| SDL      | >= 2.0.8               |
+----------+------------------------+
| SDL_mixer| >= 2.0.0               |
+----------+------------------------+
| SDL_image| >= 2.0.2               |
+----------+------------------------+
| SDL_ttf  | >= 2.0.12              |
+----------+------------------------+
| SDL_gfx  | (Optional, vendored in)|
+----------+------------------------+
| NumPy    | >= 1.6.2 (Optional)    |
+----------+------------------------+



Licence
-------

La bibliothèque est distribuée sous la licence `GNU LGPL version 2.1`_, qui
peut être retrouvée dans le fichier ``docs/LGPL.txt``. Nous nous réservons
le droit de placer les futures versions de cette bibliothèque sous une licence
différente.

Ceci veut en quelque sorte dire que vous êtes habilité à utiliser pygame-ce
dans n’importe quel projet que souhaitez, mais que si vous voulez effectuer des 
changements ou des ajouts à pygame lui-même, alors vous serez dans l’obligation
de les publier avec une licence compatible (de préférence en les soumettant au projet
pygame). Les codes propriétaires et les jeux commerciaux sont autorisés.

Les programmes présents dans le sous-répertoire ``examples`` appartiennent 
au domaine public.

Voir les docs/licences pour les licences des dépendances.


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

.. _pygame: https://pyga.me
.. _Simple DirectMedia Layer: https://www.libsdl.org
.. _We need your help: https://www.pygame.org/contribute.html
.. _Compilation wiki page: https://github.com/pygame-community/pygame-ce/wiki#compiling
.. _docs page: https://pyga.me/docs
.. _GNU LGPL version 2.1: https://www.gnu.org/copyleft/lesser.html

.. _简体中文: README.zh-cn.rst
.. _English: ./../../README.rst
.. _فارسی: README.fa.rst