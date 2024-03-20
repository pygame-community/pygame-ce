.. TUTORIAL: Ajuda! Como eu movo uma imagem?

.. include:: ../../common.txt

******************************************************
  Tutoriais Pygame - Ajuda! Como eu movo uma imagem?
******************************************************

Ajuda! Como eu movo uma imagem?
==============================

.. rst-class:: docinfo

:Author: Pete Shinners
:Contact: pete@shinners.org

Muitas pessoas novas na programação e gráficos têm dificuldade em entender
como fazer uma imagem se mover na tela. Sem entender todos os conceitos, pode ser muito confuso. Você não é a primeira pessoa a ficar presa aqui, farei o meu melhor para explicar as coisas passo a passo. Até tentaremos terminar com métodos para manter suas animações eficientes.

Observe que não vamos ensiná-lo a programar com Python neste artigo, apenas apresentar alguns conceitos básicos com o Pygame.

Apenas Pixels na Tela
---------------------

O Pygame possui uma superfície de exibição (Surface). Isso é basicamente uma imagem visível na tela, e a imagem é composta por pixels. A principal maneira de alterar esses pixels é chamando a função blit(). Isso copia os pixels de uma imagem para outra.

Isso é a primeira coisa a entender. Quando você faz blit em uma imagem na tela, você está simplesmente mudando a cor dos pixels na tela. Os pixels não são adicionados ou movidos, apenas alteramos as cores dos pixels que já estão na tela. As imagens que você faz blit na tela também são Surfaces no Pygame, mas de nenhuma forma estão conectadas à Surface de exibição. Quando elas são blitadas na tela, são copiadas para a exibição, mas você ainda tem uma cópia única da original.

Com essa breve descrição, talvez você já consiga entender o que é necessário para "mover" uma imagem. Na verdade, não movemos nada. Simplesmente fazemos blit da imagem em uma nova posição. Mas antes de desenharmos a imagem na nova posição, precisaremos "apagar" a antiga. Caso contrário, a imagem será visível em dois lugares na tela. Rapidamente apagando a imagem e redesenhando-a em um novo local, conseguimos a "ilusão" de movimento.

Ao longo deste tutorial, dividiremos esse processo em etapas mais simples. Explicaremos também as melhores maneiras de ter várias imagens se movendo pela tela. Você provavelmente já tem perguntas. Como, por exemplo, como "apagamos" a imagem antes de desenhá-la em uma nova posição? Talvez você ainda esteja completamente perdido? Bem, espero que o restante deste tutorial possa esclarecer as coisas para você.

Voltando um Passo
-----------------

Talvez o conceito de pixels e imagens ainda seja um pouco estranho para você? Bem, boas notícias, nas próximas seções vamos usar um código que faz tudo o que queremos, apenas não usa pixels. Vamos criar uma pequena lista Python com 6 números e imaginaremos que ela representa alguns gráficos fantásticos que poderíamos ver na tela. Pode ser surpreendente o quanto isso representa exatamente o que faremos mais tarde com gráficos reais.

Vamos começar criando nossa lista de tela e preenchendo-a com uma paisagem bonita de 1s e 2s. ::

  >>> screen = [1, 1, 2, 2, 2, 1]
  >>> print(screen)
  [1, 1, 2, 2, 2, 1]

Agora criamos nosso plano de fundo. Não será muito emocionante a menos que também desenhemos um jogador na tela. Vamos criar um herói poderoso que se parece com o número 8. Vamos colocá-lo perto do meio do mapa e ver como fica. ::

  >>> screen[3] = 8
  >>> print(screen)
  [1, 1, 2, 8, 2, 1]

Isso pode ser tão longe quanto você chegou se começou a programar gráficos com o Pygame. Você tem algo bonito na tela, mas ele não pode se mover para lugar nenhum. Talvez agora que nossa tela é apenas uma lista de números, seja mais fácil entender como movê-lo?

Fazendo o Herói Se Mover
------------------------

Antes de começarmos a mover o personagem, precisamos manter o controle de alguma posição para ele. Na última seção, quando o desenhamos, escolhemos uma posição arbitrária. Vamos fazer isso um pouco mais oficial desta vez. ::

  >>> playerpos = 3
  >>> screen[playerpos] = 8
  >>> print(screen)
  [1, 1, 2, 8, 2, 1]

Agora é bastante fácil movê-lo para uma nova posição. Simplesmente alteramos o valor de `playerpos` e o desenhamos na tela novamente. ::

  >>> playerpos = playerpos - 1
  >>> screen[playerpos] = 8
  >>> print(screen)
  [1, 1, 8, 8, 2, 1]

Ops. Agora podemos ver dois heróis. Um na posição antiga e outro na nova posição. Esta é exatamente a razão pela qual precisamos "apagar" o herói em sua posição antiga antes de desenhá-lo na nova posição. Para apagá-lo, precisamos mudar esse valor na lista de volta para o que era antes de o herói estar lá. Isso significa que precisamos acompanhar os valores na tela antes de o herói substituí-los. Existem várias maneiras de fazer isso, mas a mais fácil geralmente é manter uma cópia separada do fundo da tela. Isso significa que precisamos fazer algumas mudanças em nosso pequeno jogo.

Criando um Mapa
---------------

O que queremos fazer é criar uma lista separada que chamaremos de nosso plano de fundo. Vamos criar o plano de fundo para que pareça com nossa tela original, com 1s e 2s. Em seguida, copiaremos cada item do plano de fundo para a tela. Depois disso, finalmente podemos desenhar nosso herói de volta na tela. ::

  >>> background = [1, 1, 2, 2, 2, 1]
  >>> screen = [0]*6                         # uma nova tela em branco
  >>> for i in range(6):
  ...     screen[i] = background[i]
  >>> print(screen)
  [1, 1, 2, 2, 2, 1]
  >>> playerpos = 3
  >>> screen[playerpos] = 8
  >>> print(screen)
  [1, 1, 2, 8, 2, 1]

Esta é uma maneira bastante fácil de criar um plano de fundo. Outra maneira é usar a função `list()` que também copia uma lista. ::

  >>> background = [1, 1, 2, 2, 2, 1]
  >>> screen = list(background)
  >>> print(screen)
  [1, 1, 2, 2, 2, 1]
  >>> playerpos = 3
  >>> screen[playerpos] = 8
  >>> print(screen)
  [1, 1, 2, 8, 2, 1]

Ambos os métodos produzirão o mesmo resultado, então você pode escolher qualquer um. Se você estiver se perguntando por que não começamos com uma nova tela em branco, isso é uma excelente pergunta. A resposta é que, à medida que seu jogo se torna mais complexo, você deseja desenhar o mínimo possível a cada quadro. Desenhar cada pixel da tela a cada quadro é bastante ineficiente. Em vez disso, se apenas desenharmos os pixels que mudaram, podemos fazer com que nosso jogo funcione muito mais rapidamente.

Limpando a Tela
-----------------

Antes de podermos desenhar nosso herói na nova posição, precisamos "apagar" seu rastro. Isso significa que precisamos desenhar o fundo de volta na posição onde o herói costumava estar. Isso significa que agora, antes de desenhar o herói, também precisamos desenhar o plano de fundo de volta na tela.

O código que faz isso é bastante fácil, podemos simplesmente copiar cada valor do plano de fundo de volta para a tela. ::

  >>> for i in range(6):
  ...     screen[i] = background[i]
  >>> print(screen)
  [1, 1, 2, 2, 2, 1]

Então, agora o herói se move um passo à esquerda. Em seguida, fazemos uma cópia do plano de fundo de volta na tela para "apagar" sua trilha. Depois disso, finalmente, desenhamos o herói na nova posição.

Encapsulando com Funções
-------------------------

Agora, é muito fácil ver como podemos encapsular isso em algumas funções. Em vez de nos preocuparmos com todos os detalhes, vamos simplesmente criar algumas funções que fazem o trabalho para nós. O primeiro será para criar o plano de fundo. ::

  >>> def createbackground():
  ...     return [1, 1, 2, 2, 2, 1]

Então, podemos chamar essa função sempre que quisermos começar um novo jogo. ::
  >>> background = createbackground()
  >>> print(background)
  [1, 1, 2, 2, 2, 1]

Outra função pode ser criada para desenhar o plano de fundo na tela. ::

  >>> def drawbackground():
  ...     for i in range(6):
  ...         screen[i] = background[i]
  ...     print(screen)

Agora, sempre que quisermos "apagar" a tela, podemos chamar esta função. ::
  >>> drawbackground()
  [1, 1, 2, 2, 2, 1]

Finalmente, podemos encapsular a movimentação do herói em uma função. ::
  >>> def movehero(position):
  ...     screen[position] = 8
  ...     print(screen)

Agora, sempre que quisermos mover o herói, podemos chamar esta função. ::
  >>> movehero(3)
  [1, 1, 2, 8, 2, 1]
  >>> movehero(2)
  [1, 1, 8, 8, 2, 1]

Esta é uma maneira bastante básica de criar um jogo simples que usa os mesmos conceitos que você precisará para mover imagens no Pygame. Claro, o Pygame faz um trabalho muito melhor gerenciando tudo para você. Em vez de criar uma lista para cada pixel, o Pygame possui objetos de `Surface` para lidar com isso. Mas o conceito é muito semelhante.

Fazendo o herói se mover (Parte 2)
---------------------------------

Desta vez será fácil movimentar o herói. Primeiro vamos apagar
o herói de sua antiga posição. Fazemos isso copiando o valor correto
do fundo para a tela. Então vamos desenhar o personagem em seu
nova posição na tela


  >>> imprimir(tela)
  [1, 1, 2, 8, 2, 1]
  >>> tela[playerpos] = background[playerpos]
  >>> playerpos = playerpos - 1
  >>> tela[playerpos] = 8
  >>> imprimir(tela)
  [1, 1, 8, 2, 2, 1]


Aí está. O herói moveu-se um espaço para a esquerda. Podemos usar isso
mesmo código para movê-lo para a esquerda novamente. ::

  >>> tela[playerpos] = background[playerpos]
  >>> playerpos = playerpos - 1
  >>> tela[playerpos] = 8
  >>> imprimir(tela)
  [1, 8, 2, 2, 2, 1]


Excelente! Isso não é exatamente o que você chamaria de animação suave. Mas com
algumas pequenas alterações, faremos isso funcionar diretamente com os gráficos no
a tela.


Definição: "blit"
-----------------

Nas próximas seções transformaremos nosso programa de usar listas para
usando gráficos reais na tela. Ao exibir os gráficos, iremos
use o termo **blit** com freqüência. Se você é novo em fazer gráficos
trabalho, você provavelmente não está familiarizado com esse termo comum.

BLIT: Basicamente, blit significa copiar gráficos de uma imagem
para outro. Uma definição mais formal é copiar uma matriz de dados
para um destino de matriz de bitmap. Você pode pensar em blit apenas como
*"atribuindo"* pixels. Muito parecido com definir valores em nossa lista de telas
acima, blitting atribui a cor dos pixels em nossa imagem.

Outras bibliotecas gráficas usarão a palavra *bitblt*, ou apenas *blt*,
mas eles estão falando sobre a mesma coisa. Basicamente é copiar
memória de um lugar para outro. Na verdade, é um pouco mais avançado do que
cópia direta da memória, já que ela precisa lidar com coisas como pixel
formatos, recorte e tons de scanline. Bliters avançados também podem
lidar com coisas como transparência e outros efeitos especiais.


Indo da lista para a tela
-------------------------

Para levar o código que vemos acima para exemplos e fazê-los funcionar com
pygame é muito simples. Vamos fingir que carregamos alguns lindos
gráficos e os nomeou "terrain1", "terrain2" e "hero". Onde antes
atribuímos números a uma lista, agora exibimos gráficos na tela. Outro
grande mudança, em vez de usar posições como um único índice (0 a 5), ​​nós
agora precisamos de uma coordenada bidimensional. Vamos fingir que cada um dos gráficos
em nosso jogo tem 10 pixels de largura. ::

  >>> plano de fundo = [terreno1, terreno1, terreno2, terreno2, terreno2, terreno1]
  >>> tela = create_graphics_screen()
  >>> para i no intervalo (6):
  ... tela.blit(fundo[i], (i*10, 0))
  >>> playerpos = 3
  >>> screen.blit(playerimage, (playerpos*10, 0))


Hmm, esse código deve parecer muito familiar e, esperançosamente, mais importante;
o código acima deve fazer algum sentido. Espero que minha ilustração de cenário
valores simples em uma lista mostram a semelhança da configuração de pixels na tela
(com blit). A única parte que realmente dá trabalho extra é converter a posição do jogador
em coordenadas na tela. Por enquanto, usamos apenas um :code:`(playerpos*10, 0)` bruto,
mas certamente podemos fazer melhor do que isso. Agora vamos mover o jogador
imagem sobre um espaço. Este código não deve ter surpresas. ::

  >>> screen.blit(background[playerpos], (playerpos*10, 0))
  >>> playerpos = playerpos - 1
  >>> screen.blit(playerimage, (playerpos*10, 0))


Aí está. Com este código mostramos como exibir um plano de fundo simples
com a imagem de um herói. Então movemos corretamente aquele herói um espaço
Para a esquerda. Então, para onde vamos a partir daqui? Bem, por um lado, o código ainda é
um pouco estranho. A primeira coisa que queremos fazer é encontrar uma maneira mais limpa de representar
o plano de fundo e a posição do jogador. Então talvez um pouco mais suave, real
animação.


Coordenadas de tela
-------------------

Para posicionar um objeto na tela, precisamos informar a função blit()
onde colocar a imagem. No pygame sempre passamos as posições como coordenadas (X,Y).
Isso representa o número de pixels à direita e o número de pixels
para baixo para colocar a imagem. O canto superior esquerdo de uma superfície é a coordenada (0,
0). Mover um pouco para a direita seria (10, 0) e depois mover para baixo apenas
tanto seria (10, 10). Ao blitting, o argumento de posição representa
onde o canto superior esquerdo da origem deve ser colocado no destino.

Pygame vem com um contêiner conveniente para essas coordenadas, é um
Reto. O Rect representa basicamente uma área retangular nessas coordenadas.
Tem canto superior esquerdo e um tamanho. O Rect vem com muitos recursos convenientes
métodos que ajudam você a movê-los e posicioná-los. Em nossos próximos exemplos iremos
representam as posições de nossos objetos com os Rects.

Saiba também que muitas funções em pygame esperam argumentos Rect. Todos esses
funções também podem aceitar uma tupla simples de 4 elementos (esquerda, superior, largura,
altura). Nem sempre você é obrigado a usar esses objetos Rect, mas você
principalmente quero. Além disso, a função blit() pode aceitar um Rect como sua posição
argumento, ele simplesmente usa o canto superior esquerdo do Rect como a posição real.


Mudando o plano de fundo
------------------------

Em todas as seções anteriores, armazenamos o plano de fundo como uma lista
de diferentes tipos de terreno. Essa é uma boa maneira de criar um jogo baseado em peças,
mas queremos uma rolagem suave. Para tornar isso um pouco mais fácil, vamos
mude o fundo para uma única imagem que cubra toda a tela. Esse
forma, quando queremos “apagar” nossos objetos (antes de redesenhá-los) só precisamos
para exibir a seção do fundo apagado na tela.

Ao passar um terceiro argumento Rect opcional para blit, dizemos ao blit para apenas
use essa subseção da imagem de origem. Você verá isso em uso abaixo, conforme
apagar a imagem do jogador.

Observe também que agora, quando terminamos de desenhar na tela, chamamos pygame.display.update()
que mostrará tudo o que desenhamos na tela.


Movimento Suave
---------------

Para fazer algo parecer se mover suavemente, queremos apenas movê-lo alguns
pixels por vez. Aqui está o código para fazer um objeto se mover suavemente
a tela. Com base no que já sabemos, isso deve parecer bem simples. ::

  >>> tela = create_screen()
  >>> clock = pygame.time.Clock() #obtém um objeto relógio pygame
  >>> jogador = load_player_image()
  >>> fundo = load_background_image()
  >>> screen.blit(background, (0, 0)) #desenhe o plano de fundo
  >>> posição = player.get_rect()
  >>> screen.blit(player, position) #desenha o jogador
  >>> pygame.display.update() #e mostre tudo
  >>> para x no intervalo (100): #animar 100 quadros
  ... screen.blit(fundo, posição, posição) #erase
  ... posição = posição.move(2, 0) #move jogador
  ... screen.blit(jogador, posição) #desenha novo jogador
  ... pygame.display.update() #e mostre tudo
  ... clock.tick(60) #update 60 vezes por segundo


Aí está. Este é todo o código necessário para animar suavemente
um objeto na tela. Podemos até usar um personagem de fundo bonito.
Outro benefício de fazer o background desta forma, a imagem para o player
pode ter transparência ou seções recortadas e ainda será desenhado corretamente
sobre o fundo (um bônus grátis).

Também fazemos uma chamada para pygame.time.Clock() para capturar o elemento clock.
Com ele, podemos chamar clock.tick() para definir a taxa de quadros em quadros por segundo.
Isto retarda um pouco o nosso programa, caso contrário ele poderá rodar tão rápido que você poderá
não vejo isso.


Então, o que vem a seguir?
--------------------------

Bem, aí está. Esperamos que este artigo tenha feito tudo o que prometeu
pendência. Mas, neste ponto, o código realmente não está pronto para o próximo best-seller
jogo. Como podemos facilmente ter vários objetos em movimento? O que exatamente são esses
funções misteriosas como load_player_image()? Também precisamos de uma maneira de simplificar
entrada do usuário e loop por mais de 100 quadros. Tomaremos o exemplo que
temos aqui, e transformá-lo em uma criação orientada a objetos que faria a mamãe
orgulhoso.


Primeiro, as funções misteriosas
--------------------------------

Informações completas sobre esses tipos de funções podem ser encontradas em outros tutoriais
e referência. O módulo pygame.image possui uma função load() que fará
o que nós queremos. As linhas para carregar as imagens devem ficar assim. ::

  >>> jogador = pygame.image.load('player.bmp').convert()
  >>> background = pygame.image.load('liquid.bmp').convert()


Podemos ver que é bem simples, a função load leva apenas um nome de arquivo
e retorna um novo Surface com a imagem carregada. Depois de carregar fazemos uma ligação
ao método Surface, convert(). Convert nos retorna uma nova superfície do
imagem, mas agora convertida para o mesmo formato de pixel da nossa exibição. Desde o
as imagens terão o mesmo formato na tela, elas desaparecerão muito rapidamente.
Se não convertemos, a função blit() é mais lenta, pois precisa converter
de um tipo de pixel para outro à medida que avança.

Você também deve ter notado que tanto load() quanto convert() retornam new
Superfícies. Isso significa que estamos realmente criando duas superfícies em cada uma dessas
linhas. Em outras linguagens de programação, isso resulta em vazamento de memória (não
uma coisa boa). Felizmente o Python é inteligente o suficiente para lidar com isso, e o pygame
limpará adequadamente a superfície que acabamos não usando.

A outra função misteriosa que vimos no exemplo acima foi create_screen().
No pygame é simples criar uma nova janela para gráficos. O código para criar
uma superfície de 640x480 está abaixo. Ao não passar nenhum outro argumento, o pygame irá apenas
escolha a melhor profundidade de cor e formato de pixel para nós. ::

  >>> tela = pygame.display.set_mode((640, 480))


Lidando com algumas entradas
----------------------------

Precisamos desesperadamente mudar o loop principal para procurar qualquer entrada do usuário (como
quando o usuário fecha a janela). Precisamos adicionar "manipulação de eventos" ao nosso
programa. Todos os programas gráficos usam esse design baseado em eventos. O programa
obtém eventos como "teclado pressionado" ou "mouse movido" do computador. Então
o programa responde aos diferentes eventos. Aqui está o que o código deve
parece. Em vez de repetir 100 quadros, continuaremos repetindo até o
o usuário nos pede para parar. ::

  >>> enquanto Verdadeiro:
  ... para evento em pygame.event.get():
  ... se event.type == pygame.QUIT:
  ... sys.exit()
  ... move_and_draw_all_game_objects()


O que esse código simplesmente faz é primeiro fazer um loop para sempre e depois verificar se há
quaisquer eventos do usuário. Saímos do programa se o usuário pressionar fechar
botão na janela. Depois de verificarmos todos os eventos, movemos e empatamos
nossos objetos de jogo. (Também iremos apagá-los antes que se movam)


Movendo múltiplas imagens
-------------------------

Esta é a parte em que realmente vamos mudar as coisas. Vamos
digamos que queremos 10 imagens diferentes se movendo na tela. Uma boa maneira de
lidar com isso é usar as classes do python. Criaremos uma classe que representa
nosso objeto de jogo. Este objeto terá a função de se mover e então
podemos criar quantos quisermos. As funções para desenhar e mover o objeto
precisam trabalhar de forma que movam apenas um quadro (ou um passo) de cada vez.
Aqui está o código python para criar nossa classe. ::

  >>> classe GameObject:
  ... def __init__(self, imagem, altura, velocidade):
  ... self.speed = velocidade
  ... self.image = imagem
  ... self.pos = image.get_rect().move(0, altura)
  ... def movimento(auto):
  ... self.pos = self.pos.move(0, self.speed)
  ... se self.pos.right > 600:
  ... self.pos.esquerda = 0


Portanto, temos duas funções em nossa classe. A função init constrói nosso objeto.
Ele posiciona o objeto e define sua velocidade. O método move move o objeto
um passo. Se for longe demais, move o objeto de volta para a esquerda.


Juntando tudo
-------------

Agora, com nossa nova classe de objeto, podemos montar o jogo inteiro. Aqui
é como será a função principal do nosso programa. ::

  >>> tela = pygame.display.set_mode((640, 480))
  >>> clock = pygame.time.Clock() #obtém um objeto relógio pygame
  >>> jogador = pygame.image.load('player.bmp').convert()
  >>> background = pygame.image.load('background.bmp').convert()
  >>> tela.blit(fundo, (0, 0))
  >>> objetos = []
  >>> para x no intervalo(10): #crie 10 objetos</i>
  ... o = GameObject(jogador, x*40, x)
  ...objetos.append(o)
  >>> enquanto Verdadeiro:
  ... para evento em pygame.event.get():
  ... se event.type == pygame.QUIT:
  ... sys.exit()
  ... para o em objetos:
  ... tela.blit(fundo, o.pos, o.pos)
  ... para o em objetos:
  ... o.move()
  ... tela.blit(o.imagem, o.pos)
  ...pygame.display.update()
  ... relógio.tick(60)


E aí está. Este é o código que precisamos para animar 10 objetos na tela.
O único ponto que talvez precise ser explicado são os dois loops que usamos para limpar
todos os objetos e desenhe todos os objetos. Para fazer as coisas corretamente,
precisamos apagar todos os objetos antes de desenhar qualquer um deles. Em nossa amostra
aqui pode não importar, mas quando os objetos estão sobrepostos, usando dois loops
assim se torna importante.


Preparando-se para obter informações aprimoradas do usuário
-----------------------------------------------------------

Com todas as entradas do teclado encerrando o programa, isso não é muito interativo.
Vamos adicionar algumas informações extras do usuário!

Primeiro devemos criar um personagem único que o jogador controlará. Nós
podemos fazer isso da mesma forma que criamos as outras entidades móveis. Vamos
chame o objeto do jogador p. Já podemos mover qualquer objeto, mas o jogador deve
têm mais informações do que simplesmente mover para a direita. Para acomodar isso, vamos renovar
nossa função move em nossa classe GameObject. ::

  >>> def move(self, up=False, down=False, left=False, right=False):
  ...   if right:
  ...       self.pos.right += self.speed
  ...   if left:
  ...       self.pos.right -= self.speed
  ...   if down:
  ...       self.pos.top += self.speed
  ...   if up:
  ...       self.pos.top -= self.speed   
  ...   if self.pos.right > WIDTH:
  ...       self.pos.left = 0
  ...   if self.pos.top > HEIGHT-SPRITE_HEIGHT:
  ...       self.pos.top = 0
  ...   if self.pos.right < SPRITE_WIDTH:
  ...       self.pos.right = WIDTH
  ...   if self.pos.top < 0:
  ...       self.pos.top = HEIGHT-SPRITE_HEIGHT

Certamente há muito mais acontecendo aqui, então vamos dar um passo de cada vez.
Primeiro, adicionamos alguns valores padrão à função move, declarada como up,
para baixo, para a esquerda e para a direita. Esses booleanos nos permitirão selecionar especificamente um
direção em que o objeto está se movendo. A primeira parte, onde passamos e
verifique True para cada variável, é onde adicionaremos a posição do objeto,
muito como antes. A direita controla a horizontal e a parte superior controla as posições verticais.

Além disso, removemos o número mágico presente anteriormente e o substituímos
com as constantes WIDTH, HEIGHT, SPRITE_WIDTH e SPRITE_HEIGHT. Esses valores
representam a largura e a altura da tela, juntamente com a largura e a altura do objeto
exibido na tela.

A segunda parte, onde a posição está sendo verificada, garante que a posição
está dentro dos limites da nossa tela. Com isso em vigor, precisamos ter certeza de que
quando um de nossos outros objetos chama move, definimos right como true.


Adicionando a entrada do usuário
--------------------------------

Já vimos que o pygame possui manipulação de eventos e sabemos que KEYDOWN é
um evento neste loop. Poderíamos, em KEYDOWN, afirmar que o pressionamento da tecla corresponde a um
tecla de seta, onde chamaríamos move. Contudo, esse movimento só ocorrerá
uma vez cada vez que uma tecla é pressionada e, portanto, será extremamente instável e
desagradável.

Para isso podemos usar pygame.key.get_pressed(), que retorna uma lista de todas as chaves,
e se eles estão ou não pressionados no momento. Como queremos que essas teclas sejam pressionadas
ser mantido quer um evento esteja acontecendo ou não, devemos colocar
fora do loop de manipulação do evento principal, mas ainda dentro do loop do jogo.
Nossa funcionalidade ficará assim. ::

  >>> chaves = pygame.key.get_pressed()
  >>> if chaves[pygame.K_UP]:
  ... p.move(up=True)
  >>> if chaves[pygame.K_DOWN]:
  ... p.move (para baixo = Verdadeiro)
  >>> if chaves[pygame.K_LEFT]:
  ... p.move(esquerda=Verdadeiro)
  >>> if chaves[pygame.K_RIGHT]:
  ... p.move(direita=Verdadeiro)

Simplesmente obtemos nossa lista de teclas pressionadas, chamadas de teclas. Podemos então verificar o índice
na posição do código-chave para ver se ele está pressionado. Para mais códigos-chave, recomendo
verificando a documentação em pygame.key.

Quando segurado para cima, movemos nosso objeto, p, para cima. Quando pressionado para baixo, descemos. Enxaguar e
repita para todos os casos e estamos prontos!


Juntando tudo mais uma vez
--------------------------

Agora que terminamos com a funcionalidade do player, vamos dar uma última olhada para fazer
certeza de que entendemos tudo. ::

  >>> tela = pygame.display.set_mode((640, 480))
  >>> clock = pygame.time.Clock() #obtém um objeto relógio pygame
  >>> jogador = pygame.image.load('player.bmp').convert()
  >>> entidade = pygame.image.load('alien1.bmp').convert()
  >>> background = pygame.image.load('background.bmp').convert()
  >>> tela.blit(fundo, (0, 0))
  >>> objetos = []
  >>> p = GameObject(player, 10, 3) #cria o objeto do jogador
  >>> para x no intervalo(10): #crie 10 objetos</i>
  ... o = GameObject(entidade, x*40, x)
  ...objetos.append(o)
  >>> enquanto Verdadeiro:
  ... chaves = pygame.key.get_pressed()
  ... se chaves[pygame.K_UP]:
  ... p.move(up=True)
  ... se chaves[pygame.K_DOWN]:
  ... p.move (para baixo = Verdadeiro)
  ... se chaves[pygame.K_LEFT]:
  ... p.move(esquerda=Verdadeiro)
  ... se chaves[pygame.K_RIGHT]:
  ... p.move(direita=Verdadeiro)
  ... para evento em pygame.event.get():
  ... se event.type == pygame.QUIT:
  ... sys.exit()
  ... para o em objetos:
  ... tela.blit(fundo, o.pos, o.pos)
  ... para o em objetos:
  ... o.move()
  ... tela.blit(o.imagem, o.pos)
  ...pygame.display.update()
  ... relógio.tick(60)

Algumas coisas não mencionadas anteriormente: carregamos uma segunda imagem e a chamamos de entidade,
e usamos isso para todos os objetos que não são o jogador, que usa o jogador
imagem definida anteriormente.

E isso é tudo! Agora temos um objeto player totalmente funcional que
é controlado usando as teclas de seta!


Você está por conta própria a partir daqui
------------------------------------------

Então, qual seria o próximo passo em seu caminho para o aprendizado? Bem, primeiro brincando
com este exemplo um pouco. A versão completa deste exemplo está disponível
no diretório de exemplos do pygame. É o exemplo nomeado
:func:`moveit.py <pygame.examples.moveit.main>` .
Dê uma olhada no código e brinque com ele, execute-o e aprenda.

Talvez você queira trabalhar em ter mais de um tipo de objeto.
Encontrar uma maneira de "excluir" objetos de maneira limpa quando você não deseja mostrá-los
não mais.

Existem também outros tutoriais e exemplos em pygame que cobrem esses
problemas. Então, quando você estiver pronto para continuar aprendendo, continue lendo. :-)

Por último, você pode ficar à vontade para acessar a lista de discussão ou sala de bate-papo do pygame
com qualquer dúvida sobre esse assunto. Sempre há pessoas disponíveis que podem ajudar
você sai com esse tipo de negócio.

Por último, divirta-se, é para isso que servem os jogos!
