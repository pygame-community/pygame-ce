.. TUTORIAL: Tutorial de Criação de Jogos com Pygame de Tom Chance

.. include:: ../../common.txt

****************************
  Criando Jogos com Pygame
****************************


Criando Jogos com Pygame
========================

.. toctree::
   :hidden:
   :glob:

   tom-games2
   tom-games3
   tom-games4
   tom-games5
   tom-games6

Sumário
-----------------

\1. :ref:`Introdução <makegames-1>`

  \1.1. :ref:`Nota sobre estilos de codificação <makegames-1-1>`

\2. :ref:`Revisão: Fundamentos do Pygame <makegames-2>`

  \2.1. :ref:`O jogo básico do pygame <makegames-2-1>`

  \2.2. :ref:`Objetos básicos do pygame <makegames-2-2>`

  \2.3. :ref:`Blitting <makegames-2-3>`

  \2.4. :ref:`O loop de eventos <makegames-2-4>`

  \2.5. :ref:`Ta-da! <makegames-2-5>`

\3. :ref:`Iniciando as coisas <makegames-3>`

  \3.1. :ref:`As primeiras linhas e carregando módulos <makegames-3-1>`

  \3.2. :ref:`Funções de manipulação de recursos <makegames-3-2>`

\4. :ref:`Classes de objetos de jogo <makegames-4>`

  \4.1. :ref:`Uma classe simples de bola <makegames-4-1>`

    \4.1.1. :ref:`Diversão 1: Sprites <makegames-4-1-1>`

    \4.1.2. :ref:`Diversão 2: Física vetorial <makegames-4-1-2>`

\5. :ref:`Objetos controláveis pelo usuário <makegames-5>`

  \5.1. :ref:`Uma classe simples de bastão <makegames-5-1>`

    \5.1.1. :ref:`Diversão 3: Eventos Pygame <makegames-5-1-1>`

\6. :ref:`Colocando tudo junto <makegames-6>`

  \6.1. :ref:`Deixe a bola atingir os lados <makegames-6-1>`

  \6.2. :ref:`Deixe a bola atingir os bastões <makegames-6-2>`

  \6.3. :ref:`O produto final <makegames-6-3>`


.. _makegames-1:

1. Introdução
-------------

Antes de mais nada, vou supor que você leu o :doc:`Tutorial Passo a Passo do Chimp <chimp-explanation>`,
que apresenta o básico do Python e pygame. Dê uma lida antes de ler este
tutorial, pois não vou me preocupar em repetir o que esse tutorial diz (pelo menos não em tanto detalhe). Este tutorial é destinado a quem
entende como fazer um "jogo" ridiculamente simples e gostaria de fazer um jogo relativamente simples como Pong.
Ele introduz alguns conceitos de design de jogos, alguma matemática simples para calcular a física da bola e algumas maneiras de manter seu
jogo fácil de manter e expandir.

Todo o código neste tutorial trabalha para implementar o `TomPong <http://tomchance.org.uk/projects/pong>`_,
um jogo que eu escrevi. No final do tutorial, você não apenas deve ter uma compreensão mais firme do pygame, mas
você também deve entender como o TomPong funciona e como fazer sua própria versão.

Agora, para um breve resumo do básico do pygame. Um método comum de organizar o código para um jogo é dividi-lo nas seguintes
seis seções:

  - **Carregar módulos** necessários no jogo. Coisas padrão, exceto que você deve
    lembrar de importar os nomes locais do pygame, além do próprio módulo pygame.

  - **Classes de manipulação de recursos**; defina algumas classes para lidar com seus recursos mais básicos,
    que serão carregar imagens e sons, bem como conectar e desconectar de e para redes, carregar salvar
    arquivos de jogos, e quaisquer outros recursos que você possa ter.

  - **Classes de objetos de jogo**; defina as classes para o objeto do seu jogo. No exemplo do pong,
    essas serão uma para o bastão do jogador (que você pode inicializar várias vezes, uma para cada jogador no jogo) e uma
    para a bola (que também pode ter várias instâncias). Se você for ter um menu agradável no jogo, também é uma boa ideia fazer uma
    classe de menu.

  - **Outras funções do jogo**; defina outras funções necessárias, como placares, menu
    manipulação, etc. Qualquer código que você possa colocar na lógica principal do jogo, mas que tornaria difícil entender essa lógica, deve
    ser colocado em sua própria função. Assim como traçar um placar não é lógica de jogo, ele deve ser movido para uma função.

  - **Inicializar o jogo**, incluindo os próprios objetos pygame, o plano de fundo, o jogo
    objetos (inicializando instâncias das classes) e quaisquer outros pedaços de código que você possa querer adicionar.

  - **O loop principal**, onde você coloca qualquer manipulação de entrada (ou seja, observando os usuários apertarem
    teclas/botões do mouse), o código para atualizar os objetos do jogo e, finalmente, para atualizar a tela.

Cada jogo que você fizer terá algumas ou todas essas seções, possivelmente com mais algumas de suas próprias. Para os propósitos deste tutorial, eu irei
escrever sobre como o TomPong está estruturado, e as ideias que escrevo podem ser transferidas para quase qualquer tipo de jogo que você possa fazer. Eu irei
também assumir que você deseja manter todo o código em um único arquivo, mas se você estiver fazendo um jogo razoavelmente grande, muitas vezes é uma boa
ideia dividir certas seções em arquivos de módulos. Colocar as classes de objetos do jogo em um arquivo chamado ``objects.py``, por exemplo, pode ajudar a manter a lógica do jogo separada dos objetos do jogo. Se você tem muito código de manipulação de recursos, também pode ser útil
colocá-lo em ``resources.py``. Você pode então :code:`from objects,resources import *` para importar todas as
classes e funções.

.. _makegames-1-1:

1.1. Nota sobre estilos de codificação
--------------------------------------

A primeira coisa a lembrar ao abordar qualquer projeto de programação é decidir sobre um estilo de codificação e permanecer consistente. Python
resolve muitos dos problemas por causa de sua interpretação rigorosa de espaços em branco e recuo, mas você ainda pode escolher o tamanho
de seus recuos, se você coloca cada importação de módulo em uma nova linha, como você comenta o código, etc. Você verá como eu faço tudo isso
nos exemplos de código; você não precisa usar meu estilo, mas seja qual for o estilo que você adotar, use-o em todo o código do programa. Tente também
documentar todas as suas classes e comentar sobre qualquer parte do código que pareça obscura, embora não comece a comentar o óbvio. Eu já vi muita gente fazer o seguinte::

  player1.score += scoreup        # Adicione scoreup ao placar do jogador1

O pior código é mal formatado, com mudanças aparentemente aleatórias no estilo e documentação fraca. Código ruim não é apenas irritante
para outras pessoas, mas também torna difícil para você manter.
