.. TUTORIAL: Escolhendo e Configurando Modos de Exibição

.. include:: ../../common.txt

********************************************************
  Tutoriais do Pygame - Configurando Modos de Exibição
********************************************************


Configurando Modos de Exibição
==============================

.. rst-class:: docinfo

:Author: Pete Shinners
:Contact: pete@shinners.org


Introdução
----------

Configurar o modo de exibição no *pygame* cria uma superfície de imagem visível
no monitor.
Essa superfície pode cobrir toda a tela ou estar em uma janela
em plataformas que suportam um gerenciador de janelas.
A superfície de exibição não é nada mais do que um objeto de superfície padrão
do *pygame*.
Existem funções especiais necessárias no módulo :mod:`pygame.display`
para manter o conteúdo da superfície de imagem atualizado no monitor.

Configurar o modo de exibição no *pygame* é uma tarefa mais fácil do que na
maioria das bibliotecas gráficas.
A vantagem é que, se o modo de exibição desejado não estiver disponível,
o *pygame* emulará o modo de exibição solicitado.
*Pygame* selecionará uma resolução de exibição e uma profundidade de cor que
melhor corresponda às configurações solicitadas,
permitindo que você acesse a exibição no formato desejado.
Na realidade, uma vez que o módulo :mod:`pygame.display` é
um envoltório em torno da biblioteca SDL, a SDL está realmente realizando
todo esse trabalho.

Existem vantagens e desvantagens em configurar o modo de exibição dessa
maneira.
A vantagem é que, se o seu jogo exigir um modo de exibição específico,
seu jogo será executado em plataformas que não suportam seus requisitos.
Também facilita quando você está começando algo,
pois é sempre fácil voltar depois e tornar a seleção do modo um pouco mais
específica.
A desvantagem é que nem sempre você obterá o que solicitou.
Há também uma penalidade de desempenho quando o modo de exibição precisa ser
emulado.
Este tutorial ajudará você a entender os diferentes métodos para consultar
as capacidades de exibição das plataformas e configurar o modo de exibição para
o seu jogo.


Princípios Básicos de Configuração
----------------------------------

A primeira coisa a aprender é como realmente configurar o modo de exibição atual.
O modo de exibição pode ser configurado a qualquer momento depois que o
módulo :mod:`pygame.display` foi inicializado.
Se você já configurou o modo de exibição anteriormente,
configurá-lo novamente alterará o modo atual.
A configuração do modo de exibição é tratada pela função
:func:`pygame.display.set_mode((largura, altura), flags, profundidade)
<pygame.display.set_mode>`.
O único argumento obrigatório nesta função é uma sequência contendo
a largura e a altura do novo modo de exibição.
A flag de profundidade é a quantidade solicitada de bits por pixel para a
superfície.
Se a profundidade fornecida for 8, o *pygame* criará uma superfície mapeada
por cores.
Quando fornecido uma profundidade de bits mais alta, o *pygame* usará um modo
de cores compactadas.
Muito mais informações sobre profundidades e modos de cores podem ser encontradas
na documentação dos módulos de exibição e superfície.
O valor padrão para a profundidade é 0.
Quando fornecido um argumento de 0, o *pygame* selecionará a melhor profundidade
de bits a ser usada, geralmente a mesma que a profundidade de bits atual do
sistema.
O argumento de flags permite controlar recursos extras para o modo de exibição.
Novamente, mais informações sobre isso são encontradas nos documentos de
referência do *pygame*.


Como Decidir
------------

Então, como selecionar um modo de exibição que funcionará melhor com seus
recursos gráficos e a plataforma em que seu jogo está sendo executado?
Existem vários métodos para obter informações sobre o dispositivo de exibição.
Todos esses métodos devem ser chamados após o módulo de exibição ter sido
inicializado, mas você provavelmente deseja chamá-los antes de definir o modo
de exibição.
Primeiro, :func:`pygame.display.Info() <pygame.display.Info>`
retornará um objeto especial do tipo VidInfo,
que pode fornecer muitas informações sobre as capacidades do driver gráfico.
A função
:func:`pygame.display.list_modes(profundidade, flags) <pygame.display.list_modes>`
pode ser usada para encontrar os modos gráficos suportados pelo sistema.
:func:`pygame.display.mode_ok((largura, altura), flags, profundidade)
<pygame.display.mode_ok>` leva os mesmos argumentos que
:func:`set_mode() <pygame.display.set_mode>`,
mas retorna a profundidade de bits mais próxima daquela que você solicita.
Por último, :func:`pygame.display.get_driver() <pygame.display.get_driver>`
retornará o nome do driver gráfico selecionado pelo *pygame*.

Apenas lembre-se da regra de ouro.
*Pygame* funcionará com praticamente qualquer modo de exibição que você
solicitar.
Alguns modos de exibição precisarão ser emulados,
o que retardará seu jogo,
já que o *pygame* precisará converter cada atualização que você fizer para o
modo de exibição "real". A melhor opção é sempre permitir que o *pygame*
escolha a melhor profundidade de bits,
e converter todos os seus recursos gráficos para esse formato quando
forem carregados.
Você permite que o *pygame* escolha sua profundidade de bits chamando
:func:`set_mode() <pygame.display.set_mode>`
sem argumento de profundidade ou uma profundidade de 0,
ou você pode chamar
:func:`mode_ok() <pygame.display.mode_ok>`
para encontrar uma profundidade de bits mais próxima do que você precisa.

Quando o modo de exibição está em janela,
geralmente você deve corresponder à mesma profundidade de bits da área de trabalho.
Quando está em tela cheia, algumas plataformas podem alternar para qualquer
profundidade de bits que melhor se adapte às suas necessidades.
Você pode encontrar a profundidade da área de trabalho atual se obter um objeto
VidInfo antes de definir o modo de exibição.

Depois de definir o modo de exibição,
você pode descobrir informações sobre suas configurações obtendo um objeto VidInfo,
ou chamando qualquer um dos métodos Surface.get* na superfície de exibição.


Funções
-------

Essas são as rotinas que você pode usar para determinar o modo de exibição mais
apropriado.
Você pode encontrar mais informações sobre essas funções na documentação do módulo
de exibição.

  :func:`pygame.display.mode_ok(size, flags, profundidade) <pygame.display.mode_ok>`

    Esta função leva exatamente os mesmos argumentos que pygame.display.set_mode().
    Retorna a melhor profundidade de bits disponível para o modo que você descreveu.
    Se isso retornar zero,
    então o modo de exibição desejado não está disponível sem emulação.

  :func:`pygame.display.list_modes(profundidade, flags) <pygame.display.list_modes>`

    Retorna uma lista de modos de exibição suportados com a profundidade e flags
    solicitados.
    Uma lista vazia é retornada quando não há modos.
    O argumento de flags padrão é :any:`FULLSCREEN <pygame.display.set_mode>`\ .
    Se você especificar suas próprias flags sem :any:`FULLSCREEN <pygame.display.set_mode>`\ ,
    você provavelmente obterá um valor de retorno de -1.
    Isso significa que qualquer tamanho de exibição está bom, já que a exibição será
    em janela.
    Note que os modos listados são ordenados do maior para o menor.

  :func:`pygame.display.Info() <pygame.display.Info>`

    Esta função retorna um objeto com muitos membros descrevendo
    o dispositivo de exibição.
    Imprimir o objeto VidInfo mostrará rapidamente todos os
    membros e valores para este objeto. ::

      >>> import pygame.display
      >>> pygame.display.init()
      >>> info = pygame.display.Info()
      >>> print(info)
      <VideoInfo(hw = 0, wm = 1,video_mem = 0
              blit_hw = 0, blit_hw_CC = 0, blit_hw_A = 0,
              blit_sw = 0, blit_sw_CC = 0, blit_sw_A = 0,
              bitsize  = 32, bytesize = 4,
              masks =  (16711680, 65280, 255, 0),
              shifts = (16, 8, 0, 0),
              losses =  (0, 0, 0, 8),
              current_w = 1920, current_h = 1080
      >

Você pode testar todas essas flags simplesmente como membros do objeto VidInfo.


Exemplos
--------

Aqui estão alguns exemplos de diferentes métodos para iniciar a exibição gráfica.
Eles devem ajudá-lo a ter uma ideia de como configurar seu modo de exibição. ::

  >>> # me dê a melhor profundidade com uma exibição em janela de 640 x 480
  >>> pygame.display.set_mode((640, 480))

  >>> # me dê a maior exibição de 16 bits disponível
  >>> modos = pygame.display.list_modes(16)
  >>> if not modos:
  ...     print('16 bits não suportados')
  ... else:
  ...     print('Resolução Encontrada:', modos[0])
  ...     pygame.display.set_mode(modos[0], FULLSCREEN, 16)

  >>> # preciso de uma superfície de 8 bits, nada mais servirá
  >>> if pygame.display.mode_ok((800, 600), 0, 8) != 8:
  ...     print('Só posso trabalhar com uma exibição de 8 bits, desculpe')
  ... else:
  ...     pygame.display.set_mode((800, 600), 0, 8)
