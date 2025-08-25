.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ `简体中文`_ **繁體中文** `Français`_ `فارسی`_ `Español`_
----

Pygame_ 是一款自由且開源的跨平台程式庫，用於開發電子遊戲等多媒體應用。Pygame基於 `Simple DirectMedia Layer library`_ 以及其他幾個廣受歡迎的程式庫，提取其中最常見的函數，讓編寫遊戲成為更符合直覺的事情。

本發行版名為 **“pygame - Community Edition“** （簡稱 “pygame-ce“）。

pygame-ce是上游pygame專案的分支，由此前pygame專案的核心開發者創建。開發者們在上游的開發中受到了強烈的阻撓，無法繼續，所以創建了這個發行版。新的發行版主旨在提供更頻繁的版本更新，持續不斷的bug修復與功能增強，以及更民主的管理模式。

歡迎新的貢獻者加入我們。

安装
------------

::

   pip install pygame-ce


入門
----

剛接觸pygame的初學者應該可以快速入門。pygame提供了大量教學與介紹，也提供了整個函式庫的完整參考文件。你可以在 `docs page`_ 瀏覽文件。也可以在終端機中執行`python -m pygame.docs`，在本機瀏覽文件。如果找不到本機文檔，會自動開啟線上文檔。

線上文件與github中的開發版pygame同步。文件版本可能比你正在使用的pygame版本新一些。在終端機中執行 ``pip install pygame-ce --upgrade`` 可以升級到最新完整版本。

最重要的是，examples目錄中有許多可以玩的小程序，可以讓你立即開啟程式碼之旅。

從原始碼開始編譯
--------------------

如果你想使用那些正在開發的特性，或者你想要為pygame做出貢獻，你需要從原始碼開始編譯pygame，而不是用pip來安裝。

編譯與安裝的流程是高度自動化的。你要做的工作主要是pygame依賴的編譯與安裝。一旦完成，你就可以執行`setup.py`，它會嘗試完成自動配置，編譯，然後安裝pygame。

更多關於編譯與安裝訊息，請參閱 `Compilation wiki page`_ 。



鳴謝
-------

感謝為本資源庫貢獻的每一個人。

特別鳴謝：

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

感謝發送補丁/修復的人：Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber,
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

以及我們卓越的bug獵人：Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau

還有許多人提交了有用的想法，助力本計畫前進，使我們的生活變得更加輕鬆。感謝你們！

非常感謝人們提出文件評論並添加到 pygame 文件和 pygame-ce 文檔

感謝製作遊戲並把遊戲放到pygame.org網站供人學習與娛樂的人。

感謝 James Paige 建立了pygame bugzilla。

感謝 Roger Dingledine 與SEUL.ORG上的crew，感謝我們優秀的主持。

依賴
------------


pygame顯然依賴SDL和Python。此外pygame也嵌入了幾個較小的函式庫：font模組依賴SDL_ttf（SDL_ttf依賴freetype）；mixer模組（以及mixer.music模組）依賴SDL_mixer；image模組依賴SDL_image（SDL_image使用到libjpeg與libpng） ；transform模組內嵌了一個SDL_rotozoom來實現它的rotozoom函式；surfarray模組用到了Numpy中的多維數組。

依賴的版本要求如下：



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


如何貢獻
--------

首先，感謝你考慮為 pygame-ce 做出貢獻！正是像你這樣的人讓 pygame-ce 成為一個偉大的函式庫。請依照以下步驟開始：

1. 閱讀 `Contribution Guidelines`_ 和 `Many Ways to Contribute`_ wiki 頁面。
2. 閱讀 `Opening A Pull Request`_ 和 `Opening a Great Pull Request`_ 的相關文件。
3. 學習How to `label and link reported issues`_ 。
4. 檢查 `issue tracker`_ 以查找你有興趣的issue，或建立一個新的issue來開始討論你的想法。

`wiki pages`_ 上還有許多資源可以幫助你入門。

如果有任何問題，請隨時在 `Pygame Community Discord Server`_ 詢問或建立一個issue。


授權條款
-------
**授權條款版本:** LGPL-2.1-or-later

本函式庫在 `GNU LGPL version 2.1`_ 下發布，許可文件： ``docs/LGPL.txt`` 。我們保留將此函式庫的未來版本置於其他許可證下的權利。

這基本上代表你可以在任意專案中使用pygame，但如果你修改或增加了pygame庫的內容，這些內容必須使用原授權條款相容的授權發布（我們更希望修改者將其提交回pygame專案）。閉源或商業性遊戲中可以使用pygame。

``examples`` 目錄中的程式不受版權限制。

有關依賴相的許可證，請參閱 ``docs/licenses`` 。



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
.. _简体中文: README.zh-cn.rst
.. _Français: README.fr.rst
.. _فارسی: README.fa.rst
.. _Español: README.es.rst
