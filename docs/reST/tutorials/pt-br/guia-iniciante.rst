.. TUTORIAL: Guia para iniciantes em Pygame de David Clark

..inclui:: ../../common.txt

**********************************
  Guia para iniciantes em Pygame
**********************************

.. title:: Um guia para iniciantes em pygame


Um guia para iniciantes em pygame
=================================

ou **Coisas que aprendi por tentativa e erro para que você não precise fazer isso,**

ou **Como aprendi a parar de me preocupar e amar a tristeza.**

Pygame_ é um wrapper python para SDL_, escrito por Pete Shinners. O que isso
significa que, usando pygame, você pode escrever jogos ou outros recursos multimídia
aplicativos em Python que serão executados inalterados em qualquer um dos SDLs suportados
plataformas (Windows, Linux, Mac e outras).

Pygame pode ser fácil de aprender, mas o mundo da programação gráfica pode ser
bastante confuso para o recém-chegado. Escrevi isso para tentar destilar o prático
conhecimento que adquiri ao longo do último ano trabalhando com pygame, e seu
predecessor, PySDL. Tentei classificar essas sugestões em ordem de
importância, mas a relevância de qualquer dica específica dependerá do seu próprio
histórico e os detalhes do seu projeto.


Sinta-se confortável trabalhando em Python
------------------------------------------

O mais importante é se sentir confiante ao usar python. Aprendendo algo
tão potencialmente complicado quanto a programação gráfica será uma verdadeira tarefa árdua se
você também não está familiarizado com o idioma que está usando. Escreva alguns
programas não gráficos em python - analise alguns arquivos de texto, escreva uma suposição
jogo ou um programa de diário ou algo assim. Fique confortável com barbante e
manipulação de listas - saiba como dividir, fatiar e combinar strings e listas.
Saiba como funciona ``import`` -- tente escrever um programa que esteja espalhado por
vários arquivos de origem. Escreva suas próprias funções e pratique a manipulação
números e caracteres; saiba como converter entre os dois. Vá direto ao ponto
onde a sintaxe para usar listas e dicionários é uma segunda natureza - você não
você deseja ter que consultar a documentação toda vez que precisar dividir uma lista ou
classificar um conjunto de chaves. Familiarize-se com o uso de caminhos de arquivo – isso será útil
mais tarde, quando você começar a carregar ativos e criar arquivos salvos.

Resista à tentação de pedir ajuda direta online quando
você se depara com problemas. Em vez disso, ligue o intérprete e brinque com o
problema por algumas horas ou use instruções de impressão e ferramentas de depuração para descobrir
o que está errado no seu código. Adquira o hábito de pesquisar as coisas no
`documentação oficial do Python`_ e pesquisando mensagens de erro no Google para descobrir o que
eles querem dizer.

Isso pode parecer incrivelmente chato, mas a confiança que você ganhará através do seu
familiaridade com python fará maravilhas quando chegar a hora de escrever seu
jogo. O tempo que você gasta tornando o código python uma segunda natureza não será nada
em comparação com o tempo que você economizará ao escrever código real.


Reconheça quais partes do pygame você realmente precisa
-------------------------------------------------------

Olhando para a confusão de classes no topo do índice de documentação do pygame
pode ser confuso. O importante é perceber que você pode fazer um ótimo
lidar com apenas um pequeno subconjunto de funções. Muitas aulas que você provavelmente nunca
uso -- em um ano, eu não toquei no ``Canal``, ``Joystick``, ``cursores``,
Funções ``surfarray`` ou ``version``.


Saiba o que é uma superfície
----------------------------

A parte mais importante do pygame é a superfície. Pense em uma superfície como um
pedaço de papel em branco. Você pode fazer muitas coisas com uma superfície - você pode
desenhe linhas nele, preencha partes dele com cores, copie imagens de e para ele e
definir ou ler cores de pixels individuais nele. Uma superfície pode ter qualquer tamanho (dentro
motivo) e você pode ter quantos quiser (novamente, dentro do razoável).
Uma superfície é especial – aquela com a qual você cria
:func:`pygame.display.set_mode()`. Esta 'superfície de exibição' representa a tela;
tudo o que você fizer aparecerá na tela do usuário.

Então, como você cria superfícies? Como mencionado acima, você cria o especial
'superfície de exibição' com ``pygame.display.set_mode()``. Você pode criar uma superfície
que contém uma imagem usando :func:`pygame.image.load()`, ou você pode fazer uma superfície
que contém texto com :func:`pygame.font.Font.render()`. Você pode até criar uma superfície que
não contém nada com :func:`pygame.Surface()`.

A maioria das funções de superfície não são críticas. Apenas aprenda :meth:`.Surface.blit()`,
:meth:`.Surface.fill()`, :meth:`.Surface.set_at()` e :meth:`.Surface.get_at()`, e você ficará bem.


Use Surface.convert()
---------------------

Quando li pela primeira vez a documentação de :meth:`.Surface.convert()`, não pensei
era algo com que eu tinha que me preocupar. 'Eu só uso PNGs, então tudo que eu
do estará no mesmo formato. Então eu não preciso de ``convert()``';. Acontece que eu
estava muito, muito errado.

TO 'formato' ao qual ``convert()`` se refere não é o formato *arquivo* (ou seja, PNG,
JPEG, GIF), é o que chamamos de 'formato pixel'. Isso se refere ao
maneira particular como uma superfície registra cores individuais em um pixel específico.
Se o formato de superfície não for igual ao formato de exibição, o SDL terá que
converta-o rapidamente para cada blit - um processo bastante demorado. Não
preocupe-se muito com a explicação; apenas observe que ``convert()`` é necessário
se você quiser obter algum tipo de velocidade com seus blits.

Como você usa a conversão? Basta chamá-lo depois de criar uma superfície com o
:func:`.image.load()` função. Em vez de apenas fazer::

surface = pygame.image.load('foo.png')

To do::

      surface = pygame.image.load('foo.png').convert()

É tão fácil. Você só precisa chamá-lo uma vez por superfície, quando carregar um
imagem do disco. Você ficará satisfeito com os resultados; Eu vejo cerca de 6x
aumente a velocidade de blitting chamando ``convert()``.

As únicas vezes que você não quer usar ``convert()`` é quando você realmente precisa
ter controle absoluto sobre o formato interno de uma imagem - digamos que você estava escrevendo
um programa de conversão de imagem ou algo assim, e você precisava garantir que o
o arquivo de saída tinha o mesmo formato de pixel do arquivo de entrada. Se você está escrevendo um
jogo, você precisa de velocidade. Use ``convert()``.


Desconfie de conselhos desatualizados, obsoletos e opcionais
------------------------------------------------------------

Pygame existe desde o início dos anos 2000 e muita coisa mudou desde então -
tanto dentro da própria estrutura quanto dentro do cenário mais amplo da computação como um
todo. Certifique-se de verificar as datas dos materiais que você lê (incluindo este guia!),
e siga os conselhos mais antigos com cautela. Aqui estão algumas coisas comuns que
destaque para mim:

** Dirty Rects e 'truques' de desempenho **

Ao ler trechos antigos da documentação ou guias do pygame on-line, você poderá ver
alguma ênfase em atualizar apenas partes da tela que estão sujas, para o
por uma questão de desempenho (neste contexto, "sujo" significa que a região mudou desde
o quadro anterior foi desenhado).

Geralmente isso envolve chamar :func:`pygame.display.update()` (com uma lista de
rects) em vez de :func:`pygame.display.flip()`, sem fundos de rolagem,
ou até mesmo não preencher a tela com uma cor de fundo em cada frame porque pygame
supostamente não consegue lidar com isso. Algumas APIs do pygame são projetadas para suportar isso
também (por exemplo, :func:`pygame.sprite.RenderUpdates`), o que gerou muitos
sentido nos primeiros anos do pygame.

Atualmente (2022), porém, a maioria dos computadores desktop modestos são poderosos o suficiente para
atualize toda a tela uma vez por quadro a 60 FPS e além. Você pode se mover
câmera ou fundos dinâmicos e seu jogo deve funcionar perfeitamente a 60 FPS. As CPUs são
mais poderoso hoje em dia, e você pode usar ``display.flip()`` sem medo.

Dito isto, ainda existem alguns raros momentos em que esta técnica antiga ainda é útil
para extrair alguns FPS extras. Por exemplo, se você precisar atualizar apenas metade da tela
superfície e tem uma imagem estacionária na outra metade. Aqui está o processo aproximado de como funciona:

Em vez de atualizar a tela inteira a cada quadro, apenas as partes que mudaram desde
o último quadro é atualizado. Você faz isso acompanhando esses retângulos em uma lista,
em seguida, chamando ``update(the_dirty_rectangles)`` no final do quadro. Em detalhe
para um sprite em movimento:

  * Coloque um pedaço do fundo sobre a localização atual do sprite, apagando-o.
  * Anexe o retângulo de localização atual do sprite a uma lista chamada dirty_rects.
  * Mova o ator.
  * Desenhe o sprite em seu novo local.
  * Anexe a nova localização do sprite à minha lista dirty_rects.
  * Chame ``display.update(dirty_rects)``

Mesmo que esta técnica não seja realmente útil para criar jogos 2D de alto desempenho com
CPUs modernas, ainda é bom estar ciente disso. Ainda existem muitas outras maneiras
acidentalmente prejudicar o desempenho do seu jogo com uma lógica de renderização mal otimizada.
Por exemplo, mesmo em hardware moderno é provavelmente muito lento chamar ``set_at`` uma vez por pixel
na superfície da tela. Estar atento ao desempenho ainda é algo que você terá que
fazer.

Simplesmente não existem muitas dicas de 'um truque legal para corrigir o desempenho do seu código'. Todo jogo
é diferente e existem problemas diferentes e algoritmos diferentes para resolvê-los
eficientemente em cada tipo de jogo. Praticamente toda vez que o código do seu jogo 2D não atinge um
taxa de quadros razoável, a causa subjacente acabou sendo um algoritmo incorreto ou um mal-entendido
de padrões fundamentais de design de jogos.

Se você estiver tendo problemas de desempenho, primeiro certifique-se de não carregar arquivos repetidamente em seu
loop do jogo e, em seguida, use uma das muitas opções para criar o perfil do seu código para descobrir o que está ocupando o
a maior parte do tempo. Quando você estiver munido de pelo menos algum conhecimento sobre por que seu jogo está lento, tente perguntar ao
internet (via google) ou a comunidade pygame se eles tiverem algoritmos melhores para ajudá-lo.

**HWSURFACE e DOUBLEBUF**

O sinalizador HWSURFACE :func:`.display.set_mode()` não faz nada nas versões 2.0.0 do pygame e
mais tarde (você pode verificar a documentação se não acredita em mim)! Não há razão para
use-o mais. Mesmo no pygame 1, seu efeito é bastante sutil e
geralmente incompreendido pela maioria dos usuários de pygame. Nunca foi uma aceleração mágica
bandeira, infelizmente.

DOUBLEBUF ainda tem alguma utilidade, mas também não é uma bandeira mágica de aceleração.

**A classe Sprite**

Você não precisa usar as classes internas :class:`.Sprite` ou :class:`.Group`
se você não quiser. Em muitos tutoriais, pode parecer que ``Sprite`` é o
"GameObject" fundamental do pygame, do qual todos os outros objetos devem derivar,
mas na realidade é basicamente apenas um wrapper em torno de um ``Rect`` e um
``Surface``, com alguns métodos adicionais de conveniência. Você pode encontrá-lo
mais intuitivo (e divertido) escrever a lógica central e as classes do seu jogo a partir de
arranhar.

**Alfa pré-multiplicado**

Usar este modo de mesclagem alfa pode aumentar ligeiramente o desempenho do blitting, até mesmo
tem sua própria `página de tutorial <tutorials/en/premultiplied-alpha>.`


Não se distraia com questões secundárias
----------------------------------------

Às vezes, novos programadores de jogos passam muito tempo se preocupando com questões que
não são realmente críticos para o sucesso do jogo. O desejo de ficar secundário
questões 'certas' são compreensíveis, mas no início do processo de criação de um jogo,
você nem consegue saber quais são as questões importantes, muito menos quais são as respostas
você deve escolher. O resultado pode ser muita prevaricação desnecessária.

Por exemplo, considere a questão de como organizar seus arquivos gráficos.
Cada quadro deve ter seu próprio arquivo gráfico ou cada sprite? Talvez todos os
os gráficos devem ser compactados em um arquivo? Muito tempo se passou
desperdiçado em muitos projetos, fazendo essas perguntas em listas de discussão, debatendo
as respostas, o perfil, etc., etc. Esta é uma questão secundária; qualquer tempo gasto
discutir isso deveria ter sido gasto na codificação do jogo real.

A conclusão aqui é que é muito melhor ter uma solução “muito boa” que
foi realmente implementado, do que uma solução perfeita que você nunca teve tempo de
escrita.


Retos são seus amigos
---------------------

O invólucro de Pete Shinners pode ter efeitos alfa interessantes e velocidades rápidas de blitting,
mas tenho que admitir que minha parte favorita do pygame é a humilde classe :class:`.Rect`.
Um retângulo é simplesmente um retângulo - definido apenas pela posição do canto superior esquerdo
canto, sua largura e sua altura. Muitas funções do pygame aceitam rects como
argumentos, e eles também aceitam 'rectstyles', uma sequência que tem os mesmos valores
como um reto. Então, se eu precisar de um retângulo que defina a área entre 10, 20 e
40, 50, posso fazer o seguinte::

     rect = pygame.Rect(10, 20, 30, 30)
     rect = pygame.Rect((10, 20, 30, 30))
     rect = pygame.Rect((10, 20), (30, 30))
     reto = (10, 20, 30, 30)
     reto = ((10, 20, 30, 30))

Se você usar qualquer uma das três primeiras versões, entretanto, você terá acesso ao Rect's
funções de utilidade. Isso inclui funções para mover, encolher e inflar retângulos,
encontre a união de dois retângulos e uma variedade de funções de detecção de colisão.

Por exemplo, suponha que eu queira obter uma lista de todos os sprites que contêm um
ponto (x, y) - talvez o jogador tenha clicado ali, ou talvez seja o ponto atual
localização de uma bala. É simples se cada sprite tiver um membro .rect - eu apenas
fazer::

     sprites_clicked = [sprite para sprite em all_my_sprites_list if sprite.rect.collidepoint(x, y)]

Os retângulos não têm outra relação com superfícies ou funções gráficas, além do
fato de que você pode usá-los como argumentos. Você também pode usá-los em lugares que
não têm nada a ver com gráficos, mas ainda precisam ser definidos como retângulos.
A cada projeto eu descubro alguns lugares novos para usar rects onde nunca pensei
Eu precisaria deles.


Não se preocupe com a detecção de colisão com pixels perfeitos
--------------------------------------------------------------

Então você tem seus sprites se movimentando e precisa saber se
eles estão esbarrando um no outro. É tentador escrever algo como o
seguindo:

  * Verifique se os retângulos estão em colisão. Se não estiverem, ignore-os.
  * Para cada pixel na área sobreposta, veja se os pixels correspondentes de ambos os sprites estão opacos. Se sim, há uma colisão.

Existem outras maneiras de fazer isso, com máscaras de sprite AND e assim por diante, mas qualquer
da maneira que você faz isso no pygame, provavelmente será muito lento. Para a maioria dos jogos,
provavelmente é melhor apenas fazer 'colisão sub-rect' - crie um retângulo para cada
sprite que é um pouco menor que a imagem real e use-o para
em vez disso, colisões. Será muito mais rápido e na maioria dos casos o jogador não
observe a imprecisão.


Gerenciando o subsistema de eventos
-----------------------------------

O sistema de eventos do Pygame é meio complicado. Na verdade, existem duas maneiras diferentes
para descobrir o que um dispositivo de entrada (teclado, mouse ou joystick) está fazendo.

A primeira é verificar diretamente o estado do dispositivo. Você faz isso por
chamando, digamos, :func:`pygame.mouse.get_pos()` ou :func:`pygame.key.get_pressed()`.
Isso lhe dirá o estado desse dispositivo *no momento em que você ligar para o
função.*

O segundo método usa a fila de eventos SDL. Esta fila é uma lista de eventos -
eventos são adicionados à lista à medida que são detectados e são excluídos da
fila enquanto são lidos.

Existem vantagens e desvantagens em cada sistema. Verificação de estado (sistema
1) fornece precisão - você sabe exatamente quando uma determinada entrada foi feita - se
``mouse.get_pressed([0])`` é 1, isso significa que o botão esquerdo do mouse está
para baixo *neste momento*. A fila de eventos apenas informa que o
o mouse caiu em algum momento no passado; se você verificar a fila com bastante frequência,
isso pode estar ok, mas se você atrasar a verificação por outro código, insira
a latência pode aumentar. Outra vantagem do sistema de verificação de estado é que ele
detecta "cordação" facilmente; isto é, vários estados ao mesmo tempo. Se você
quiser saber se as teclas ``t`` e ``f`` estão pressionadas ao mesmo tempo, basta
verificar::

     if key.get_pressed[K_t] and key.get_pressed[K_f]:
         print("Yes!")

No sistema de filas, entretanto, cada pressionamento de tecla chega na fila como um
evento completamente separado, então você precisa lembrar que a chave ``t`` foi
para baixo, e ainda não tinha subido, enquanto verificava a tecla ``f``. Um pouco mais
complicado.

O sistema estatal tem, contudo, uma grande fraqueza. Ele apenas informa o que
o estado do dispositivo está no momento em que é chamado; se o usuário clicar no mouse
botão então o libera logo antes de uma chamada para ``mouse.get_pressed()``, o
o botão do mouse retornará 0 -- ``get_pressed()`` perdeu o pressionamento do botão do mouse
completamente. Os dois eventos, ``MOUSEBUTTONDOWN`` e ``MOUSEBUTTONUP``, serão
ainda estará na fila do evento, esperando para ser recuperado e
processado.

A lição é: escolha o sistema que atenda às suas necessidades. Se você não
tem muita coisa acontecendo em seu loop -- digamos que você está sentado em um ``while True``
loop, aguardando entrada, use ``get_pressed()`` ou outra função de estado; o
a latência será menor. Por outro lado, se cada pressionamento de tecla for crucial, mas
a latência não é tão importante - digamos que seu usuário esteja digitando algo em uma caixa de edição,
use a fila de eventos. Algumas teclas pressionadas podem demorar um pouco, mas pelo menos você
pegue todos eles.

Uma observação sobre ``event.poll()`` vs. ``wait()`` -- ``poll()`` pode parecer melhor,
já que não impede que seu programa faça nada enquanto espera
input -- ``wait()`` suspende o programa até que um evento seja recebido.
Entretanto, ``poll()`` consumirá 100% do tempo disponível da CPU enquanto for executado,
e preencherá a fila de eventos com ``NOEVENTS``. Use ``set_blocked()`` para
selecione apenas os tipos de eventos de seu interesse - sua fila será muito
mais gerenciável.

Outra observação sobre a fila de eventos – mesmo que você não queira usá-la, você deve
ainda limpe-o periodicamente porque ainda estará cheio de eventos
em segundo plano enquanto o usuário pressiona as teclas e passa o mouse sobre a janela. No Windows,
se o seu jogo demorar muito sem limpar a fila, o sistema operacional irá
acho que travou e mostra a mensagem "O aplicativo não está respondendo".
Iterando sobre ``event.get()`` ou simplesmente chamando ``event.clear()`` uma vez por quadro
evitará isso.


Colorkey vs. Alfa
-----------------

Há muita confusão em torno desses dois termos, e muito disso vem
partir da terminologia utilizada.

Alfa por pixel é o melhor tipo de alfa para usar, ele lhe dará um ótimo
bordas transparentes e 'emplumadas'. Basicamente, cada pixel na imagem de origem
tem seu próprio valor alfa, de 0 a 255. A maioria dos editores de imagem permite exportar
imagens com canal alfa e pygame podem carregá-las.

'Colorkey blitting' envolve dizer ao pygame que todos os pixels de uma determinada cor
em uma determinada imagem são transparentes em vez de qualquer cor que tenham.
Esses pixels transparentes não são apagados quando o resto da imagem é apagado,
e assim não obscureça o fundo. Basta chamar :meth:`.Surface.set_colorkey()`,
e passe uma tupla RGB - digamos (0,0,0). Isso faria com que cada pixel na fonte
imagem transparente em vez de preta. Costumava ser significativamente mais barato fazer blit
do que por pixel alfa, mas este não é mais o caso e em muitos casos é
na verdade mais lento.

A superfície 'Alpha' também está disponível e se aplica a toda a superfície. Alfa de superfície
faz com que cada pixel na imagem de origem seja apenas *parcialmente* opaco.
Por exemplo, se você definir o alfa de uma superfície como 192 e depois transferi-lo para um
fundo, 3/4 da cor de cada pixel viria da imagem de origem e 1/4
do fundo. Alpha é medido de 255 a 0, onde 0 é completamente
transparente e 255 é completamente opaco. Observe que a superfície alfa e alfa
blitting pode ser combinado.


Arquitetura de software, padrões de design e jogos
--------------------------------------------------

Você pode chegar a um ponto em que se sinta confortável em escrever código e seja capaz de resolver
problemas complexos sem assistência, você entende como usar a maioria dos recursos do pygame
módulos e, ainda assim, à medida que você trabalha em projetos maiores, eles sempre parecem ficar mais confusos
e mais difícil de manter com o passar do tempo. Isto pode se manifestar de muitas maneiras - por
por exemplo, consertar bugs em um lugar pode sempre parecer criar novos bugs em outro lugar,
descobrir *para onde* o código deve ir pode se tornar um desafio, adicionando novos
muitas vezes, as coisas podem exigir que você reescreva muitas outras coisas e assim por diante.
Finalmente, você decide reduzir suas perdas e começar do zero em algo novo.

Este é um problema comum e pode ser frustrante. Por um lado, o seu
as habilidades de programação estão melhorando, mas você não consegue terminar os jogos
você começa devido a problemas organizacionais um tanto nebulosos.

Isso nos leva ao conceito de arquitetura de software e padrões de design. Você
pode estar familiarizado com o modelo base "padrão" do pygame (existem muitos equivalentes
variações disso, então não se estresse muito com os pequenos detalhes):

.. code-block:: python
   :caption: Standard Pygame game loop
   :name: game_loop.py
   :linenos:

    import pygame

    pygame.init()

    screen = pygame.display.set_mode((1280,720))

    clock = pygame.time.Clock()

    running = True

    while running:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Do logical updates here.
        # ...

        screen.fill("purple")  # Fill the display with a solid color

        # Render the graphics here.
        # ...

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)         # wait until next frame (at 60 FPS)

    pygame.quit()

Ele faz algumas configurações iniciais, inicia um loop e então prossegue repetidamente
coletar informações, lidar com a lógica do jogo e desenhar o quadro atual para sempre até
o programa termina. O loop de atualização, renderização e espera mostrado aqui é na verdade um design
padrão que serve como esqueleto da maioria dos jogos - é prolífico porque é
limpo, é organizado e funciona. (Há também um importante, mas fácil de perder
recurso de design aqui na forma de uma divisão estrita entre a lógica do jogo
e rotinas de renderização. Esta decisão por si só impede toda uma categoria de potenciais
bugs relacionados à atualização e renderização de objetos simultaneamente, o que é bom).

Acontece que existem muitos padrões de design como esse que são usados com frequência
em jogos e no desenvolvimento de software em geral. Para obter um ótimo recurso sobre isso
especificamente para jogos, eu recomendo `Game Programming Patterns`_, um breve
e-book gratuito sobre o tema. Abrange vários padrões úteis e situações concretas
onde você pode querer empregá-los. Isso não fará de você um programador melhor instantaneamente,
mas aprender alguma teoria sobre arquitetura de software pode ajudar muito
ajudando você a escapar de estagnações e enfrentar projetos maiores com mais confiança.


Faça as coisas do jeito python
------------------------------

Uma nota final (esta não é a menos importante; apenas vem no final).
Pygame é um wrapper bastante leve em torno do SDL, que por sua vez é um recurso bastante
wrapper leve em torno das chamadas gráficas do seu sistema operacional nativo. As chances são lindas
é bom que se o seu código ainda estiver lento e você tiver feito as coisas que mencionei
acima, o problema está na maneira como você aborda seus dados em python.
Certos idiomas serão lentos em python, não importa o que você faça.
Felizmente, python é uma linguagem muito clara – se um trecho de código parecer estranho ou
pesado, é provável que sua velocidade também possa ser melhorada. Leia `Por que o Pygame é
Slow`_ para uma visão mais profunda sobre por que o pygame pode ser considerado mais lento que
outros frameworks/mecanismos e o que isso realmente significa na prática.
E se você está realmente perplexo com problemas de desempenho, criadores de perfil como cProfile_
(ou SnakeViz_, um visualizador para cProfile) pode ajudar a identificar gargalos (eles
informar quais partes do código estão demorando mais para serem executadas). Dito isto,
a otimização prematura é a raiz de todos os males; se já for rápido o suficiente,
não torture o código tentando torná-lo mais rápido. Se for rápido o suficiente, deixe
ser :)

Ai está. Agora você sabe praticamente tudo que precisa sobre como usar o pygame.
Agora, vá escrever esse jogo! ;)

------

*David Clark é um ávido usuário de pygame e editor do Pygame Code
Repositório, uma vitrine para código de jogo python enviado pela comunidade. Ele é também
o autor de Twitch, um jogo de arcade de pygame totalmente mediano.*

*Este guia foi substancialmente atualizado em 2022 e atualizado novamente em 2023.*

.. _Pygame: https://pyga.me/
.. _SDL: http://libsdl.org
.. _Python documentation: https://docs.python.org/3/
.. _Game Programming Patterns: https://gameprogrammingpatterns.com/contents.html
.. _Why Pygame is Slow: https://blubberquark.tumblr.com/post/630054903238262784/why-pygame-is-slow
.. _cProfile: https://docs.python.org/3/library/profile.html
.. _SnakeViz: https://jiffyclub.github.io/snakeviz/