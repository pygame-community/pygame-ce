.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :width: 800
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English` `简体中文`_ `繁體中文`_ `Français`_ `فارسی`_ `Español`_ **日本語** `Italiano`_ `Русский`_

---------------------------------------------------------------------------------------------------

Pygame_ は、Pythonを使ってビデオゲームのようなマルチメディアアプリケーションを
開発するための、フリーでオープンソースなクロスプラットフォームライブラリです。
`Simple DirectMedia Layer library`_ や他のいくつかの有名なライブラリを使って、
最も一般的な機能を抽象化して、これらのプログラムの作成をより直感的な作業にします。

このディストリビューションは **'pygame - Community Edition'** (略して 'pygame-ce')と呼ばれます。


これは、以前のコア開発者たちによって作られた pygame プロジェクトのフォークであり、
アップストリームの開発を継続できなくなるという困難な状況の後に作成されました。
この新しいディストリビューションは、より頻繁なリリース、継続的なバグ修正や機能強化、
そしてより民主的なガバナンスモデルを提供することを目指しています。

新しいコントリビュータは歓迎されています！


インストール
------------

::

   pip install pygame-ce


ヘルプ
------

pygame を初めて使用する場合、すぐに開始できるはずです。
Pygame には多くのチュートリアルや入門資料が付属しています。
また、ライブラリ全体の完全なリファレンスドキュメントもあります。
`docs page`_ でドキュメントを参照できます。

また、端末で ``python -m pygame.docs`` を実行することで、
ドキュメントを参照することもできます。もしローカルのドキュメントが
見つからない場合は、オンラインのウェブサイトが代わりに表示されます。

オンラインドキュメントは、github の pygame の開発版に最新の状態で
追従しています。これは、あなたが使用している pygame のバージョンよりも
少し新しいかもしれません。最新の完全リリースにアップグレードするには、
端末で ``pip install pygame-ce --upgrade`` を実行してください。


最も重要なことは、examples ディレクトリに多くのプレイ可能な
小さなプログラムがあり、そのコードによって今すぐ使い始められることです。

すぐにコードを使い始めることができることです。


ソースからのビルド
------------------

現在開発中の機能を使用したい場合や、pygame-ce に貢献したい場合は、
pip インストールするのではなく、ソースコードからローカルで
pygame-ce をビルドする必要があります。

ソースからのインストールはかなり自動化されています。
作業のほとんどは、pygame の依存関係をすべてコンパイルして
インストールすることです。それが終われば、 ``setup.py`` スクリプトを
実行してください。自動設定、ビルド、および pygame のインストールが
試みられます。

インストールとコンパイルについてのより多くの情報は、
`Compilation wiki page`_ にあります。


謝辞
----

このライブラリの開発に貢献して下さったすべての人に感謝します。

Special thanks:

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

パッチやフィックスを送って下さった皆様: Niki Spahiev, Gordon
Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias
Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya,
Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber,
Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan,
Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine,
Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske,
Cambell Barton.

そして卓越した我々のバグハンター: Angus, Guillaume Proux, Frank
Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck,
Michael Benfield, David Lau

他にも、多くのアイデアを提案したり、プロジェクトの進行を支えたり、
我々の生活をより楽にして下さった方々がいます。ありがとう！


ドキュメントにコメントを寄せて下さったり、 `pygame documentation`_ と
`pygame-ce documentation`_ に追記して下さった方々にも感謝します。

また、ゲームを作成して、他の人が学んだり楽しんだりできるように
pygame.org ウェブサイトに投稿して下さった方々にもとても感謝します。


James Paige には、pygame の bugzilla をホスティングして下さったことを
感謝します。

Roger Dingledine と SEUL.ORG のクルーにも、優れたホスティングを
提供して下さったことを感謝します。


依存関係
--------

Pygame は、当然ながら SDL と Python に強く依存します。
また、他のいくつかの小さなライブラリにもリンクしたり、埋め込まれています。
フォントモジュールは SDL_ttf に依存しており、これは freetype に依存しています。
ミキサー（および mixer.music）モジュールは SDL_mixer に依存しています。
イメージモジュールは SDL_image に依存しています。
Transform.rotozoom には SDL_rotozoom の埋め込みバージョンが含まれており、
gfxdraw には SDL_gfx の埋め込みバージョンが含まれています。

依存バージョン:

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


コントリビュータになるには
--------------------------

最初に、pygame-ce のコントリビュータになることを考慮してくれたことに感謝します。
あなたのような方のおかげで pygame-ce を素晴らしいライブラリにすることができます。
まずは、以下のステップに従ってください:

1. `Contribution Guidelines`_ と `Many Ways to Contribute`_ wiki ページをお読みください
2. `Opening A Pull Request`_ と `Opening a Great Pull Request`_ のドキュメントをお読みください
3. `label and link reported issues`_ の How-to をお読みください
4. `issue tracker`_ で興味のある issue があるかどうかをチェックするか、
   あなたのアイデアについての議論を開始するため、新しい issue を開いてください

`wiki pages`_ にもあなたのスタートを手助けするたくさんの資料があります。
もし何か疑問があれば、issue を開くか、 `Pygame Community Discord Server`_ でお気軽にご質問ください。


ライセンス
----------

**License Identifier:** LGPL-2.1-or-later


このライブラリは `GNU LGPL version 2.1`_ ライセンスで配布されています。
ライセンスは ``docs/LGPL.txt`` にあります。我々はこのライブラリの
将来のバージョンに異なるライセンスを適用する権利を保留しています。

これは、基本的にあなたは pygame をあらゆるプロジェクトで使用できることを
意味しますが、あなたが pygame 自体に変更や追加を加えた場合、それらは
互換性のあるライセンスでリリースされることが必要です。
(できれば pygame-ce プロジェクトに送ってください)
クローズドソースや商用ゲームで使用することができます。

``examples`` サブディレクトリに含まれるプログラムはパブリックドメインです。

ライセンスの依存関係については、docs/licenses を参照してください。

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
.. _Italiano: README.it.rst
.. _Русский: README.ru.rst
