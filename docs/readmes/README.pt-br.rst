.. image:: https://raw.githubusercontent.com/pygame-community/pygame-ce/main/docs/reST/_static/pygame_logo.svg
  :alt: pygame
  :target: https://pyga.me/


|DocsStatus| 
|PyPiVersion| |PyPiLicense|
|Python3| |GithubCommits| |BlackFormatBadge|

`English`_ `简体中文`_ `Français`_ `فارسی`_ `Español`_ **Português-br**
---------------------------------------------------------------------------------------------------

O Pygame_ é uma biblioteca gratuita e de código aberto, multiplataforma, para o desenvolvimento de aplicações multimídia, como jogos de vídeo, utilizando Python. Ele utiliza a biblioteca `Simple DirectMedia Layer`_ e várias outras bibliotecas populares para abstrair as funções mais comuns, tornando a escrita desses programas uma tarefa mais intuitiva.

Esta distribuição é chamada de **'pygame - Edição da Comunidade'** ('pygame-ce' para abreviar).

É um fork do projeto pygame principal por seus antigos desenvolvedores principais e foi criado depois de desafios impossíveis impedirem a continuação do desenvolvimento no projeto principal. A nova distribuição visa oferecer lançamentos mais frequentes, correções contínuas de bugs e aprimoramentos, e um modelo de governança mais democrático.

Novos colaboradores são bem-vindos!


Instalação
----------

::

   pip install pygame-ce


Ajuda
-----

Se você está começando com o pygame, deverá conseguir começar bastante rapidamente. O pygame vem com muitos tutoriais e introduções. Também há documentação de referência completa para toda a biblioteca. Consulte a documentação na página `docs`_. Você também pode consultar a documentação localmente executando ``python -m pygame.docs`` no seu terminal. Se a documentação não for encontrada localmente, ela abrirá o site online.

A documentação online é atualizada com a versão de desenvolvimento do pygame no GitHub. Isso pode ser um pouco mais recente do que a versão do pygame que você está usando. Para atualizar para a última versão completa, execute ``pip install pygame-ce --upgrade`` no seu terminal.

O melhor de tudo, o diretório de exemplos possui muitos programas pequenos jogáveis que podem ajudá-lo a começar a brincar com o código imediatamente.


Compilação a Partir do Código Fonte
-----------------------------------

Se você deseja usar recursos que estão atualmente em desenvolvimento ou deseja contribuir para o pygame-ce, será necessário compilar o pygame-ce localmente a partir do código fonte, em vez de instalá-lo via pip.

A instalação a partir do código fonte é bastante automatizada. O trabalho mais significativo envolverá compilar e instalar todas as dependências do pygame. Uma vez feito isso, execute o script ``setup.py``, que tentará autoconfigurar, compilar e instalar o pygame.

Muito mais informações sobre instalação e compilação estão disponíveis na página do wiki de `Compilação`_.


Créditos
--------

Agradecemos a todos que ajudaram a contribuir para esta biblioteca. Agradecimentos especiais também são devidos a:

* Marcus Von Appen: muitas mudanças e correções, mantenedor do FreeBSD 1.7.1+
* Lenard Lindstrom: mantenedor do Windows 1.8+, muitas mudanças e correções
* Brian Fisher pelo construtor automático svn, rastreador de bugs e muitas contribuições
* Rene Dudfield: muitas mudanças e correções, gerente/mantenedor de lançamento 1.7+
* Phil Hassey pelo trabalho no site pygame.org
* DR0ID pelo trabalho no módulo sprite
* Richard Goedeken pela função smoothscale
* Ulf Ekström pelo código de detecção de colisão pixel perfeito
* Pete Shinners: autor original
* David Clark pela posição de braço direito
* Ed Boraas e Francis Irving: pacotes Debian
* Maxim Sobolev: empacotamento FreeBSD
* Bob Ippolito: portabilidade macOS e OS X (muito trabalho!)
* Jan Ekhol, Ray Kelm e Peter Nicolai: lidando com ideias de design iniciais
* Nat Pryce por iniciar nossos testes unitários
* Dan Richter pelo trabalho de documentação
* TheCorruptor por seus incríveis logotipos e gráficos
* Nicholas Dudfield: muitas melhorias nos testes
* Alex Folkner para pygame-ctypes

Agradecimentos aos que enviam correções e correções: Niki Spahiev, Gordon Tyler, Nathaniel Pryce, Dave Wallace, John Popplewell, Michael Urman, Andrew Straw, Michael Hudson, Ole Martin Bjoerndalen, Herve Cauwelier, James Mazer, Lalo Martins, Timothy Stranex, Chad Lester, Matthias Spiller, Bo Jangeborg, Dmitry Borisov, Campbell Barton, Diego Essaya, Eyal Lotem, Regis Desgroppes, Emmanuel Hainry, Randy Kaelber Matthew L Daniel, Nirav Patel, Forrest Voight, Charlie Nolan, Frankie Robertson, John Krukoff, Lorenz Quack, Nick Irvine, Michael George, Saul Spatz, Thomas Ibbotson, Tom Rothamel, Evan Kroske, Cambell Barton.

E nossos caçadores de bugs acima e além: Angus, Guillaume Proux, Frank Raiser, Austin Henry, Kaweh Kazemi, Arturo Aldama, Mike Mulcheck, Michael Benfield, David Lau

Há muitas outras pessoas por aí que enviaram ideias úteis, mantiveram este projeto em andamento e basicamente tornaram nossa vida mais fácil. Obrigado!

Muitos agradecimentos às pessoas que fazem comentários na documentação e contribuem para a `documentação do pygame`_ e a `documentação do pygame-ce`_.

Também muitos agradecimentos às pessoas que criam jogos e os colocam no site pygame.org para que outros possam aprender e aproveitar.

Muitos agradecimentos a James Paige por hospedar o bugzilla do pygame.

Também um grande obrigado a Roger Dingledine e à equipe da SEUL.ORG pela nossa excelente hospedagem.

Dependências
------------

O Pygame obviamente depende fortemente do SDL e do Python. Ele também se vincula e incorpora várias outras bibliotecas menores. O módulo de fontes depende do SDL_ttf, que depende do freetype. Os módulos mixer (e mixer.music) dependem do SDL_mixer. O módulo de imagem depende do SDL_image. Transform.rotozoom possui uma versão incorporada de SDL_rotozoom, e gfxdraw possui uma versão incorporada de SDL_gfx. Versões de dependência:

+----------+------------------------+
| CPython  | >= 3.8 (ou use PyPy3)  |
+----------+------------------------+
| SDL      | >= 2.0.10              |
+----------+------------------------+
| SDL_mixer| >= 2.0.4               |
+----------+------------------------+
| SDL_image| >= 2.0.4               |
+----------+------------------------+
| SDL_ttf  | >= 2.0.15              |
+----------+------------------------+


Licença
-------

Esta biblioteca é distribuída sob a `versão 2.1 da GNU LGPL`_, que pode ser encontrada no arquivo ``docs/LGPL.txt``. Reservamos o direito de colocar futuras versões desta biblioteca sob uma licença diferente.

Isso basicamente significa que você pode usar o pygame em qualquer projeto que desejar, mas se fizer quaisquer alterações ou adições ao próprio pygame, essas devem ser lançadas com uma licença compatível (preferencialmente enviadas de volta para o projeto pygame-ce). Jogos de código fechado e comerciais são permitidos.

Os programas no subdiretório ``examples`` estão no domínio público.

Consulte docs/licenses para as licenças das dependências.


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

.. _Pygame: https://pyga.me
.. _documentação do pygame-ce: https://pyga.me/docs/
.. _documentação do pygame: https://www.pygame.org/docs/
.. _biblioteca Simple DirectMedia Layer: https://www.libsdl.org
.. _página do wiki de compilação: https://github.com/pygame-community/pygame-ce/wiki#compiling
.. _página de docs: https://pyga.me/docs
.. _versão 2.1 da GNU LGPL: https://www.gnu.org/copyleft/lesser.html

.. _简体中文: ./docs/readmes/README.zh-cn.rst
.. _Français: ./docs/readmes/README.fr.rst
.. _فارسی: ./docs/readmes/README.fa.rst
.. _Español: ./docs/readmes/README.es.rst
