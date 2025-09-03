.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :width: 800
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ `简体中文`_ `繁體中文`_ `Français`_ `فارسی`_ `Español`_ `日本語`_ `Italiano`_ `Русский`_ **Ελληνικά** `Português (Brasil)`_
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

To Pygame_ είναι μια ελεύθερη και ανοικτού κώδικα βιβλιοθήκη πολλαπλών πλατφορμών.
Χρησιμοποιεί το `Simple DirectMedia Layer library`_ και πολλές άλλες
δημοφιλείς βιβλιοθήκες για να χρησιμοποιήσει αφαιρετικά τις περισσότερες βασικές συναρτήσεις,
κάνοντας έτσι τη γραφή αυτών των προγραμμάτων μια πιο διαισθητική εργασία.

Αυτή η διανομή(distribution) ονομάζεται **'pygame - Community Edition'** ('pygame-ce' για συντομία).

Είναι μια διακλάδωση(fork) από το αποθετήριο προέλευσης(upstream) του project pygame από τους πρώην κεντρικούς προγραμματιστές,
και δημιουργήθηκε μετά από απίθανες προκλήσεις που τους απέτρεψαν να συνεχίσουν την ανάπτυξη στο αποθετήριο προέλευσης(upstream).
Η νέα διανομή(distribution) στοχεύει στο να προσφέρει πιο συνεχή εκδόσεις, πολλαπλές διορθώσεις σφαλμάτων και βελτιώσεις,
και ένα πιο δημοκρατικό μοντέλο διακυβέρνησης.

Νέοι συνεισφέροντες είναι ευπρόσδεκτοι!


Εγκατάσταση
------------

::

   pip install pygame-ce


Βοήθεια
----

Αν μόλις ξεκινάτε με το pygame, θα πρέπει να
ξεκινήσετε σχετικά εύκολα. Το pygame έρχεται με αρκετά βοηθητικά υλικά
και εισαγωγές. Επίσης υπάρχουν αρκετές αναφορές στις τεκμηριώσεις
όλης της βιβλιοθήκης. Ξεφυλλίστε τις τεκμηριώσεις στο `docs page`_. Επιπλέον
μπορείτε να ξεφυλλίσετε τις τεκμηριώσεις τοπικά εκτελώντας
``python -m pygame.docs`` στο τερματικό σας. Αν οι τεκμηριώσεις δεν βρεθούν
τοπικά, θα ανοίξει την διαδικτυακή ιστοσελίδα.

Η διαδικτυακή τεκμηρίωση παραμένει ενημερωμένη με την έκδοση ανάπτυξης
του pygame στο github. Ίσως είναι λίγο νεότερη από την έκδοση του pygame
που χρησιμοποιείς. Για να αναβαθμίσεις στην τελευταία έκδοση, εκτελέστε
``pip install pygame-ce --upgrade`` στο τερματικό σας.

Το καλύτερο από όλα, ο κατάλογος με τα παραδείγματα έχει αρκετά εκτελέσιμα μικρά προγράμματα.
όπου μπορούν να σε κάνουν να αρχίσεις να ασχολείσαι κατευθείαν με τον κώδικα.


Μεταγλώττιση από τον πηγαίο κώδικα
--------------------

Αν θέλεις να χρησιμοποιείς χαρακτηριστικά τα οποία είναι σε ανάπτυξη
ή θέλεις να συνεισφέρεις στο pygame-ce, θα πρέπει να μεταγλωττίσεις το pygame-ce
τοπικά από τον πηγαίο κώδικα, αντί για την εγκατάσταση μέσω pip.

Η εγκατάσταση απο τον πηγαίο κώδικα είναι κυρίως αυτοματοποίημένη. Η περισσότερη δουλέια θα
εμπλέκει μεταγλώττιση και εγκατάσταση των εξαρτήσεων του pygame. Μόλις
ολοκληρωθεί, τρέξτε το setup.py script που θα προσπαθήσει να
προσαρμοστή αυτόματα, μεταγλωττίσει και εγκαταστήσει το pygame.

Περισσότερες πληροφορίες σχετικά με την εγκατάσταση και τη μεταγλώττιση είναι διαθέσιμες
στο `Compilation wiki page`_.


Ευχαριστίες
-------

Ευχαριστούμε όλους όσους έχουν βοηθήσει συνεισφέροντας στην βιβλιοθήκη.
Ιδιαίτερες ευχαριστίες είναι επίσης στη σειρά.


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

Ευχαριστούμε όσους στέλνουν διορθώσεις και επιδιορθώσεις: Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber,
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

Και στους κυνηγούς σφαλμάτων μας που ξεπερνούν κάθε προσδοκία: Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau

Είναι αρκετοί άλλοι που έχουν υποβάλει βοηθητικές ιδέες, κρατώντας
το project να συνεχίσει, και βασικά έχουν κάνει τη ζωή μας πιο εύκολη. Ευχαριστούμε!

Πολλές ευχαριστίες σε όσους κάνουν σχόλια στην τεκμηρίωση και προσθέτουν στο
`pygame documentation`_ και στο `pygame-ce documentation`_.

Επίσης πολλές ευχαριστίες σε όσους δημιουργούν παιχνίδια και τα ανεβάζουν στην
pygame.org ιστοσελίδα ώστε άλλοι να μάθουν και να τα απολαύσουν.

Πολλές ευχαριστίες στον James Paige για τη φιλοξενία του pygame bugzilla.

Επίσης ένα μεγάλο ευχαριστώ στον Roger Dingledine και την ομάδα στο SEUL.ORG για την εξαιρετική
φιλοξενία μας.


Εξαρτήσεις
------------

Το pygame είναι προφανώς δυνατά εξαρτημένο από SDL και Python. Επίσης
συνδέει και ενσωματώνει διάφορες άλλες μικρές βιβλιοθήκες. Το πρόγραμμα
της γραμματοσειράς βασίζεται στο SDL_ttf, το οποίο είναι εξαρτημένο από το freetype. Τα mixer
(και mixer.music) προγράμματα βασίζονται στο SDL_mixer. Το πρόγραμμα της εικόνας
βασίζεται στο SDL_image. Το Transform.rotozoom έχει μια ενσωματωμένη έκδοση
του SDL_rotozoom, και το gfxdraw έχει μια ενσωματωμένη έκδοση του SDL_gfx.
Έκδοσεις εξαρτήσεων:


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

Πώς να συνεισφέρεται
-----------------
Πρώτα απ’ όλα, σας ευχαριστούμε που σκέφτεστε να συνεισφέρετε στο pygame-ce! Είναι άνθρωποι σαν κι εσάς που κάνουν το pygame-ce μια εξαιρετική βιβλιοθήκη. Παρακαλούμε ακολουθήστε τα παρακάτω βήματα για να ξεκινήσετε:

1. Διαβάστε το `Contribution Guidelines`_ και `Many Ways to Contribute`_ wiki σελίδες.
2. Διαβάστε τις τεκμηριώσεις στο `Opening A Pull Request`_ και `Opening a Great Pull Request`_.
3. Διαβάστε το πως να `label and link reported issues`_.
4. Τσεκάρετε το `issue tracker`_ για ανοιχτά προβλήματα που σας ενδιαφέρουν ή ανοίξτε δικό σας πρόβλημα για να ξεκινήσετε μια συζήτηση σχετικά με την ιδέα σας.

Υπάρχουν πολλά ακόμα μέσα στο `wiki pages`_ που μπορούν να σας βοηθήσουν να ξεκινήσετε.

Αν έχετε οποιεσδήποτε ερωτήσεις, μη διστάσετε να ρωτήσετε στο `Pygame Community Discord Server`_ ή να ανοίξετε ένα θέμα.

Άδεια
-------
**License Identifier:** LGPL-2.1-or-later

Αυτή η βιβλιοθήκη διανέμεται υπό την άδεια `GNU LGPL version 2.1`_, η οποία
βρίσκεται στο αρχείο ``docs/LGPL.txt``.  Διατηρούμε το δικαίωμα να θέσουμε
μελλοντικές εκδόσεις αυτής της βιβλιοθήκης υπό διαφορετική άδεια.

Αυτό σημαίνει ουσιαστικά ότι μπορείτε να χρησιμοποιείτε το pygame σε οποιοδήποτε project θέλετε,
αλλά αν κάνετε οποιεσδήποτε αλλαγές ή προσθήκες στο ίδιο το pygame, αυτές πρέπει να
κυκλοφορήσουν με συμβατή άδεια (κατά προτίμηση να υποβληθούν πίσω στο pygame-ce project). Τα
κλειστά προγράμματα και τα εμπορικά παιχνίδια είναι αποδεκτά.

Τα προγράμματα στο ``examples`` υποφάκελο βρίσκονται στο δημόσιο τομέα.

Δείτε τα docs/licenses για τις άδειες των εξαρτήσεων.


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

.. _简体中文: README.zh-cn.rst
.. _繁體中文: README.zh-tw.rst
.. _English: ./../../README.rst
.. _Français: README.fr.rst
.. _فارسی: README.fa.rst
.. _Español: README.es.rst
.. _日本語: README.ja.rst
.. _Italiano: README.it.rst
.. _Русский: README.ru.rst
.. _Português (Brasil): README.pt_BR.rst
