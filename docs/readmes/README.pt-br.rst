.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_ce_logo.svg
  :width: 800
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus|
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ `简体中文`_ `繁體中文`_ `Français`_ `فارسی`_ `Español`_ `日本語`_ `Italiano`_ `Русский`_ `Ελληνικά`_ **Português (Brasil)**
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Pygame_ é uma biblioteca gratuita e de código aberto, multiplataforma,
para o desenvolvimento de aplicações multimídia, como videogames, usando Python.
Ela utiliza a `Simple DirectMedia Layer library`_ e várias outras bibliotecas
populares para abstrair as funções mais comuns, tornando a escrita
desses programas uma tarefa mais intuitiva.

Essa distribuição é chamada **'pygame - Community Edition'** (abreviado como 'pygame-ce').

É um fork do projeto pygame original, criado por antigos desenvolvedores principais,
e surgiu após desafios impossíveis impedirem a continuação do desenvolvimento upstream.
A nova distribuição tem como objetivo oferecer lançamentos mais frequentes, correções e melhorias contínuas,
além de um modelo de governança mais democrático.

Novos contribuidores são bem-vindos!


Instalação
----------

::

   pip install pygame-ce


Ajuda
-----

Se você está começando com pygame, deve conseguir iniciar rapidamente.
O Pygame vem com muitos tutoriais e introduções.
Também há documentação completa de referência para toda a biblioteca.
Consulte a documentação na `página de docs`_.
Você também pode acessar a documentação localmente executando
``python -m pygame.docs`` no terminal.
Se os docs não forem encontrados localmente, será aberto o site oficial.

A documentação online é atualizada com a versão de desenvolvimento
do pygame no GitHub. Isso pode ser um pouco mais recente que a versão do pygame
que você está usando. Para atualizar para o último lançamento completo, rode:
``pip install pygame-ce --upgrade`` no terminal.

O melhor de tudo é que o diretório de exemplos contém vários pequenos programas jogáveis
que permitem brincar com o código imediatamente.


Compilando do Código-Fonte
--------------------------

Se você deseja usar funcionalidades que estão em desenvolvimento,
ou contribuir para o pygame-ce, precisará compilar o pygame-ce
localmente a partir do código-fonte, em vez de instalar via pip.

A instalação a partir do código-fonte é bastante automatizada.
A maior parte do trabalho envolve compilar e instalar todas as dependências do pygame.
Depois disso, execute o script ``setup.py``, que tentará
auto-configurar, compilar e instalar o pygame.

Mais informações sobre instalação e compilação estão disponíveis
na `página de compilação do wiki`_.


Créditos
--------

Obrigado a todos que ajudaram a contribuir com esta biblioteca.
Agradecimentos especiais também são devidos.

* Marcus Von Appen: muitas mudanças e correções, mantenedor FreeBSD 1.7.1+
* Lenard Lindstrom: mantenedor Windows 1.8+, muitas mudanças e correções
* Brian Fisher: construtor automático svn, rastreador de bugs e muitas contribuições
* Rene Dudfield: muitas mudanças e correções, gerente de lançamentos/mantenedor 1.7+
* Phil Hassey: pelo trabalho no site pygame.org
* DR0ID: pelo trabalho no módulo sprite
* Richard Goedeken: pela função smoothscale
* Ulf Ekström: pelo código de detecção de colisão pixel-perfect
* Pete Shinners: autor original
* David Clark: pelo apoio como braço direito
* Ed Boraas e Francis Irving: pacotes Debian
* Maxim Sobolev: empacotamento FreeBSD
* Bob Ippolito: port para macOS e OS X (muito trabalho!)
* Jan Ekhol, Ray Kelm, e Peter Nicolai: por aguentarem ideias de design iniciais
* Nat Pryce: por iniciar nossos testes unitários
* Dan Richter: pelo trabalho de documentação
* TheCorruptor: pelos logos e gráficos incríveis
* Nicholas Dudfield: por muitas melhorias nos testes
* Alex Folkner: pelo pygame-ctypes

Agradecimentos a todos que enviaram patches e correções:
Niki Spahiev, Gordon Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman,
Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier,
James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias Spiller,
Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya, Eyal Lotem,
Regis Desgroppes, Emmanuel Hainry, Randy Kaelber, Matthew L Daniel, Nirav Patel,
Forrest Voight, Charlie Nolan, Frankie Robertson, John Krukoff, Lorenz Quack,
Nick Irvine, Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel,
Evan Kroske, Cambell Barton.

E aos caçadores de bugs que foram além: Angus, Guillaume Proux, Frank Raiser, Austin Henry,
Kaweh Kazemi, Arturo Aldama, Mike Mulcheck, Michael Benfield, David Lau.

Há muitas outras pessoas que enviaram ideias úteis, mantiveram este projeto vivo e
basicamente tornaram nossa vida mais fácil. Obrigado!

Muito obrigado também a todos que fizeram comentários na documentação, contribuíram para a
`documentação do pygame`_ e a `documentação do pygame-ce`_.

E obrigado a todos que criam jogos e os publicam no site pygame.org para que outros possam aprender e se divertir.

Muitos agradecimentos a James Paige por hospedar o bugzilla do pygame.
E um grande obrigado a Roger Dingledine e à equipe do SEUL.ORG pelo excelente serviço de hospedagem.


Dependências
------------

O Pygame depende fortemente do SDL e do Python.
Também faz uso e incorpora várias outras bibliotecas menores.
O módulo de fontes depende do SDL_ttf, que depende do freetype.
Os módulos mixer (e mixer.music) dependem do SDL_mixer.
O módulo image depende do SDL_image.
Transform.rotozoom contém uma versão embutida do SDL_rotozoom,
e gfxdraw contém uma versão embutida do SDL_gfx.
Versões de dependências:

+----------+------------------------+
| CPython  | >= 3.10 (Ou use PyPy3) |
+----------+------------------------+
| SDL      | >= 2.0.14              |
+----------+------------------------+
| SDL_mixer| >= 2.0.4               |
+----------+------------------------+
| SDL_image| >= 2.0.4               |
+----------+------------------------+
| SDL_ttf  | >= 2.0.15              |
+----------+------------------------+


Como Contribuir
---------------

Antes de tudo, obrigado por considerar contribuir com o pygame-ce!
São pessoas como você que tornam o pygame-ce uma ótima biblioteca.
Siga estes passos para começar:

1. Leia as `Diretrizes de Contribuição`_ e a página de wiki `Muitas Formas de Contribuir`_.
2. Leia a documentação sobre `Abrindo um Pull Request`_ e `Abrindo um Pull Request de Qualidade`_.
3. Leia como `rotular e vincular issues reportadas`_.
4. Confira o `rastreador de issues`_ para ver as issues abertas que te interessam ou abra uma nova issue para iniciar uma discussão sobre sua ideia.

Existem muitos outros recursos nas `páginas do wiki`_ que podem ajudar você a começar.

Se tiver dúvidas, sinta-se à vontade para perguntar no `Servidor Discord da Comunidade Pygame`_ ou abrir uma issue.


Licença
-------

**Identificador de Licença:** LGPL-2.1-or-later

Esta biblioteca é distribuída sob a `GNU LGPL versão 2.1`_, que pode ser encontrada no arquivo ``docs/LGPL.txt``.
Reservamos o direito de disponibilizar versões futuras desta biblioteca sob uma licença diferente.

Isso basicamente significa que você pode usar pygame em qualquer projeto que quiser,
mas se fizer alterações ou adições ao próprio pygame, estas
devem ser lançadas com uma licença compatível (de preferência submetidas
de volta ao projeto pygame-ce). Jogos comerciais e de código fechado são permitidos.

Os programas no subdiretório ``examples`` estão em domínio público.

Veja em docs/licenses as licenças das dependências.


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
.. _documentação do pygame-ce: https://pyga.me/docs/
.. _documentação do pygame: https://www.pygame.org/docs/
.. _Simple DirectMedia Layer library: https://www.libsdl.org
.. _página de compilação do wiki: https://github.com/pygame-community/pygame-ce/wiki#compiling
.. _página de docs: https://pyga.me/docs
.. _GNU LGPL versão 2.1: https://www.gnu.org/copyleft/lesser.html
.. _Diretrizes de Contribuição: https://github.com/pygame-community/pygame-ce/wiki/Contribution-guidelines
.. _Muitas Formas de Contribuir: https://github.com/pygame-community/pygame-ce/wiki/Many-ways-to-contribute
.. _Abrindo um Pull Request: https://github.com/pygame-community/pygame-ce/wiki/Opening-a-pull-request
.. _Abrindo um Pull Request de Qualidade: https://github.com/pygame-community/pygame-ce/wiki/Opening-a-great-pull-request
.. _rastreador de issues: https://github.com/pygame-community/pygame-ce/issues
.. _rotular e vincular issues reportadas: https://github.com/pygame-community/pygame-ce/wiki/Labelling-&-linking-reported-issues
.. _Servidor Discord da Comunidade Pygame: https://discord.gg/pygame
.. _páginas do wiki: https://github.com/pygame-community/pygame-ce/wiki

.. _English: ./../../README.rst
.. _简体中文: README.zh-cn.rst
.. _繁體中文: README.zh-tw.rst
.. _Français: README.fr.rst
.. _فارسی: README.fa.rst
.. _Español: README.es.rst
.. _日本語: README.ja.rst
.. _Italiano: README.it.rst
.. _Русский: README.ru.rst
.. _Ελληνικά: README.gr.rst
.. _Português (Brasil): README.pt-br.rst
