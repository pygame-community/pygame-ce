.. TUTORIAL: Introdução ao Módulo Sprite

.. include:: ../../common.txt

*****************************************************
  Tutoriais do Pygame - Introdução ao Módulo Sprite
*****************************************************


Introdução ao Módulo Sprite
===========================

.. rst-class:: docinfo

:Author: Pete Shinners
:Contact: pete@shinners.org

A versão 1.3 do Pygame vem com um novo módulo, ``pygame.sprite``. Este módulo é
escrito em Python e inclui algumas classes de nível superior para gerenciar seus
objetos de jogo. Ao usar este módulo em seu potencial total, você pode gerenciar e
desenhar facilmente seus objetos de jogo. As classes de sprite são muito otimizadas,
então é provável que seu jogo funcione mais rápido com o módulo sprite do que sem.

O módulo sprite também é destinado a ser muito genérico. Acontece que você pode usá-lo
com quase qualquer tipo de jogabilidade. Toda essa flexibilidade vem com uma pequena
penalidade, é necessário um pouco de compreensão para usá-lo corretamente. A
:mod:`documentação de referência <pygame.sprite>` para o módulo sprite pode ajudar
você a continuar, mas provavelmente precisará de um pouco mais de explicação sobre como usar
``pygame.sprite`` em seu próprio jogo.

Vários exemplos do pygame (como "chimp" e "aliens") foram atualizados para
usar o módulo sprite. Você pode querer dar uma olhada neles primeiro para ver o que é
esse módulo sprite. O módulo chimp até tem seu próprio tutorial linha por linha,
o que pode ajudar a entender melhor a programação com python
e pygame.

Observe que esta introdução pressupõe que você tenha um pouco de experiência
programando com python e está um pouco familiarizado com as diferentes partes de
criar um jogo simples. Neste tutorial, a palavra "referência" é ocasionalmente
usada. Isso representa uma variável python. Variáveis em python são referências,
então você pode ter várias variáveis apontando para o mesmo objeto.

Lição de História
-----------------

O termo "sprite" é um resquício de computadores mais antigos e de máquinas de jogos. Essas
máquinas antigas não conseguiam desenhar e apagar gráficos normais rápido o suficiente para que
eles funcionassem como jogos. Essas máquinas tinham hardware especial para lidar com objetos
de jogo que precisavam ser animados muito rapidamente. Esses objetos eram chamados de
"sprites" e tinham limitações especiais, mas podiam ser desenhados e atualizados muito
rapidamente. Eles geralmente existiam em buffers de sobreposição especiais no vídeo. Hoje em dia,
os computadores se tornaram geralmente rápidos o suficiente para lidar com objetos semelhantes
a sprites sem hardware dedicado. O termo sprite ainda é usado para representar praticamente
qualquer coisa em um jogo 2D que é animada.

As Classes
----------

O módulo sprite vem com duas classes principais. A primeira é :class:`Sprite
<pygame.sprite.Sprite>`, que deve ser usada como uma classe base para todos os seus objetos de jogo.
Esta classe não faz realmente nada por conta própria, ela apenas inclui
várias funções para ajudar a gerenciar o objeto de jogo. O outro tipo de classe é
:class:`Group <pygame.sprite.Group>`. A classe ``Group`` é um contêiner para
diferentes objetos ``Sprite``. Existem na verdade vários tipos diferentes de
classes de grupos. Alguns dos ``Groups`` podem desenhar todos os elementos que contêm,
por exemplo.

Isso é realmente tudo. Começaremos com uma descrição do que cada
tipo de classe faz e, em seguida, discutiremos as maneiras adequadas de usar essas duas classes.


A Classe Sprite
---------------

Como mencionado anteriormente, a classe Sprite foi projetada para ser uma classe base para todos
os seus objetos de jogo. Você não pode realmente usá-lo sozinho, pois ele tem apenas vários
métodos para ajudar a trabalhar com as diferentes classes de ``Group``. O sprite mantém
o controle dos grupos aos quais pertence.
O construtor da classe (método ``__init__``) recebe um argumento de um
``Group`` (ou lista de ``Groups``) ao qual a instância de ``Sprite`` deve pertencer.
Você também pode alterar a associação de ``Group`` para o ``Sprite`` com o
:meth:`add() <pygame.sprite.Sprite.add>` e
:meth:`remove() <pygame.sprite.Sprite.remove>`.
Há também um método :meth:`groups() <pygame.sprite.Sprite.groups>`,
que retorna uma lista dos grupos atuais contendo o sprite.

Ao usar suas classes de Sprite, é melhor pensar nelas como "válidas" ou
"ativas" quando pertencem a um ou mais ``Groups``. Quando você remove a
instância de todos os grupos, o pygame irá limpar o objeto. (A menos que você tenha seu
próprias referências à instância em outro lugar.) O método :meth:`kill()
<pygame.sprite.Sprite.kill>` remove o sprite de todos os grupos aos quais
pertence. Isso apagará limparmente o objeto sprite. Se você já montou alguns
jogos pequenos, saberá que às vezes excluir limparmente um objeto de jogo pode ser
complicado. O sprite também vem com um método :meth:`alive()
<pygame.sprite.Sprite.alive>`, que retorna verdadeiro se ainda for um
membro de algum grupo.


A Classe Group
--------------

A classe ``Group`` é apenas um contêiner simples. Semelhante ao sprite, ele tem
um método :meth:`add() <pygame.sprite.Group.add>` e :meth:`remove()
<pygame.sprite.Group.remove>` que podem alterar quais sprites pertencem
ao grupo. Você também pode passar um sprite ou uma lista de sprites para o construtor
(método ``__init__``) para criar uma instância de ``Group`` que contenha alguns
sprites iniciais.


O ``Group`` tem alguns outros métodos como :meth:`empty()
<pygame.sprite.Group.empty>`, para remover todos os sprites do grupo, e
:meth:`copy() <pygame.sprite.Group.copy>`, que retornará uma cópia do grupo
com todos os mesmos membros. Além disso, o método :meth:`has()
<pygame.sprite.Group.has>` verificará rapidamente se o ``Group`` contém um sprite ou uma lista de
sprites.

A outra função que você usará frequentemente é o método :meth:`sprites()
<pygame.sprite.Group.sprites>`. Isso retorna um objeto que pode ser
percorrido para acessar cada sprite que o grupo contém. Atualmente, isso é apenas um
lista dos sprites, mas em versões futuras do Python, isso provavelmente usará
iteradores para melhor desempenho.

Como atalho, o ``Group`` também tem um método :meth:`update()
<pygame.sprite.Group.update>`, que chamará um método ``update()`` em
cada sprite do grupo, passando os mesmos argumentos para cada um. Normalmente, em um
jogo, você precisa de alguma função que atualize o estado de um objeto de jogo. É muito
fácil chamar seus próprios métodos usando o método ``Group.sprites()``, mas este é
um atalho que é usado o suficiente para ser incluído. Observe também que a classe base
``Sprite`` tem um método de espaço reservado ``update()`` que aceita qualquer tipo de
argumento e não faz nada.

Por fim, o Grupo tem alguns outros métodos que permitem que você o use com
a função embutida ``len()``, obtendo o número de sprites que ele contém, e
o operador "verdade", que permite verificar se o
grupo tem algum sprite com "if meu grupo:".


Misturando-os Juntos
--------------------

Neste ponto, as duas classes parecem bastante básicas. Não fazem muito mais do que você
pode fazer com uma lista simples e sua própria classe de objetos de jogo. Mas há
algumas grandes vantagens em usar o ``Sprite`` e o ``Group`` juntos. Um sprite
pode pertencer a quantos grupos você quiser. Lembre-se de que, assim que não pertencer a nenhum
grupo, geralmente será limpo (a menos que você tenha outras referências "não de grupo"
para esse objeto).

A primeira coisa importante é uma maneira rápida e simples de categorizar sprites. Por exemplo,
digamos que tivemos um jogo semelhante ao Pacman. Poderíamos fazer grupos separados para os diferentes
tipos de objetos no jogo. Fantasmas, Pac e Pellets. Quando o Pac come um poder
pellet, podemos alterar o estado para todos os objetos fantasma afetando tudo
no grupo Ghost. Isso é mais rápido e simples do que passar por uma lista
de todos os objetos do jogo e verificar quais são fantasmas.

Adicionar e remover grupos e sprites entre eles é uma operação muito rápida
mais rápida do que usar listas para armazenar tudo. Portanto, você pode
mudar as associações de grupo de forma muito eficiente. Grupos podem ser usados para funcionar como
atributos simples para cada objeto de jogo. Em vez de rastrear algum atributo como
"perto_do_jogador" para um monte de objetos inimigos, você poderia adicioná-los a um
grupo separado. Então, quando você precisar acessar todos os inimigos que estão perto do
jogador, você já tem uma lista deles, em vez de percorrer uma lista de todos os
inimigos, verificando a flag "perto_do_jogador". Mais tarde em seu jogo, você poderia
adicionar múltiplos jogadores e, em vez de adicionar mais atributos "perto_do_jogador2",
"perto_do_jogador3", você pode facilmente adicioná-los a diferentes grupos para
cada jogador.

Outro benefício importante de usar os ``Sprites`` e ``Groups`` é que os grupos
lidam limparmente com a exclusão (ou eliminação) de objetos de jogo. Em um jogo onde muitos
objetos estão referenciando outros objetos, às vezes excluir um objeto pode ser o
mais difícil, pois ele não pode desaparecer até que não seja referenciado por ninguém. Diga
que temos um objeto que está "perseguindo" outro objeto. O perseguidor pode manter um
simples grupo que referencia o objeto (ou objetos) que está perseguindo. Se o
objeto sendo perseguido for destruído, não precisamos nos preocupar em
notificar o perseguidor para parar de perseguir. O perseguidor pode ver por si mesmo que seu
grupo agora está vazio e talvez encontrar um novo alvo.

Novamente, a coisa a lembrar é que adicionar e remover sprites de grupos é
uma operação muito barata/rápida. Você pode ser melhor adicionando muitos grupos para
conter e organizar seus objetos de jogo. Alguns deles podem até ser vazios por grandes
partes do jogo, não há penalidades para gerenciar seu jogo assim.


Os Muitos Tipos de Grupo
------------------------

Os exemplos e razões acima para usar ``Sprites`` e ``Groups`` são apenas a ponta
do iceberg. Outra vantagem é que o módulo sprite vem com vários
tipos diferentes de ``Groups``. Esses grupos todos funcionam como um
``Group`` comum, mas também têm funcionalidades adicionadas (ou funcionalidades um pouco diferentes).
Aqui está uma lista das classes ``Group`` incluídas no
módulo sprite.

  :class:`Group <pygame.sprite.Group>`

    Este é o grupo padrão "sem firulas" principalmente explicado acima. A maioria dos
    outros ``Groups`` é derivada deste, mas nem todos.

  :class:`GroupSingle <pygame.sprite.GroupSingle>`

    Isso funciona exatamente como a classe ``Group`` comum, mas contém apenas
    o sprite mais recentemente adicionado. Portanto, quando você adiciona um sprite a este grupo,
    ele "esquece" qualquer sprite anterior que tinha. Portanto, sempre contém
    apenas um ou nenhum sprite.

  :class:`RenderUpdates <pygame.sprite.RenderUpdates>`

    Este grupo é herdado de ``Group``, mas altera o
    método ``draw()`` para também retornar uma lista de pygame ``Rects``,
    que representam todas as áreas na tela que foram alteradas.
    Geralmente, você não precisa usar este grupo, mas ele está incluído para
    completude.

Essa é a lista de grupos diferentes disponíveis. Falaremos mais sobre esses
grupos de renderização na próxima seção. Não há nada impedindo você de
misturar e combinar esses grupos de renderização em seu jogo. Você definitivamente deve usar
múltiplos grupos de renderização quando quiser fazer camadas com seus sprites. Também se a tela estiver dividida
em várias seções, talvez cada seção da tela deva usar um
grupo de renderização apropriado?


Detecção de Colisão
-------------------

O módulo sprite também vem com duas funções de detecção de colisão muito genéricas.
Para jogos mais complexos, essas realmente não funcionarão para você, mas você
pode facilmente pegar o código-fonte delas e modificá-las conforme necessário.

Aqui está um resumo do que são e o que fazem.

  :func:`spritecollide(sprite, group, dokill) -> list <pygame.sprite.spritecollide>`

    Isso verifica colisões entre um único sprite e os sprites em um grupo.
    Ele requer um atributo "rect" para todos os sprites usados. Ele retorna uma lista de
    todos os sprites que se sobrepõem com o primeiro sprite. O argumento "dokill" é um
    argumento booleano. Se for verdadeiro, a função chamará o método ``kill()``
    em todos os sprites. Isso significa que a última referência a cada sprite provavelmente está na
    lista retornada. Uma rápida exemplo de uso disso em um loop ::

      >>> for bomba em sprite.spritecollide(jogador, bombas, 1):
      ...     som_explosao.play()
      ...     Explosao(bomba, 0)

    Isso encontra todos os sprites no grupo "bomba" que colidem com o jogador.
    Devido ao argumento "dokill", ele exclui todas as bombas que colidiram. Para cada
    bomba que colidiu, ele reproduz um efeito sonoro de "boom" e cria um novo
    ``Explosao`` onde a bomba estava. (Observe que a classe ``Explosao`` aqui sabe adicionar
    cada instância à classe apropriada, então não precisamos armazená-la em uma
    variável, essa última linha pode parecer um pouco "engraçada" para você, programadores python.)

  :func:`groupcollide(group1, group2, dokill1, dokill2) -> dictionary <pygame.sprite.groupcollide>`

    Isso é semelhante à função ``spritecollide``, mas um pouco mais complexo.
    Ele verifica colisões para todos os sprites em um grupo, nos sprites em
    outro. Há um argumento ``dokill`` para os sprites em cada lista. Quando
    ``dokill1`` é verdadeiro, os sprites colidentes em ``group1`` serão ``kill()``ados.
    Quando ``dokill2`` é verdadeiro, obtemos os mesmos resultados para ``group2``. O
    dicionário que ele retorna funciona assim; cada chave no dicionário é um sprite
    de ``group1`` que teve uma colisão. O valor para essa chave é uma lista dos
    sprites com os quais ele colidiu. Talvez outro exemplo de código rápido o explique
    melhor::

      >>> para alienígena em sprite.groupcollide(alienígenas, tiros, 1, 1).keys()
      ...     som_explosao.play()
      ...     Explosao(alienígena, 0)
      ...     mortes += 1

    Este código verifica as colisões entre as balas do jogador e todos os alienígenas
    que elas podem interceptar. Neste caso, apenas iteramos sobre as chaves do dicionário, mas
    poderíamos iterar sobre os ``values()`` ou ``items()`` se quiséssemos fazer algo
    mais complexo. Por exemplo, poderíamos querer reproduzir um efeito sonoro
    diferente dependendo do tipo de bala, ou talvez contar quantos alienígenas cada
    bala atingiu. Se quisermos fazer mais do que matar alienígenas e contá-los, talvez
    nós apenas quisessem derrubá-los ao invés de excluí-los completamente.
    (Aqui, temos um pequeno problema, que talvez faça sentido. Se as balas derrubassem
    os alienígenas, não gostaríamos de excluí-los, então teríamos que passar
    ``False`` para o argumento ``dokill1``, e depois loopar e ``kill()``ar aqueles que queremos
    eliminar.)

A Detecção de Colisão de sprite a sprite, e especialmente a detecção de colisão de grupo a grupo, é uma
operação cara. Você provavelmente só deve usar essas funções se realmente precisar deles.
Se seu jogo tiver muitas colisões para verificar a cada quadro, então você deve estar pensando
em otimizar ou tentar uma técnica diferente para detecção de colisão. A pior parte é
que essas funções fazem muitos loops aninhados. Eles tentam ser inteligentes sobre isso e
usar ``Rect`` collision detection onde podem, mas ainda pode ser bastante caro. Se seu
jogo é relativamente pequeno e simples, e você está apenas começando, essas funções
de colisão de sprite a sprite são provavelmente boas o suficiente.

Espero que esta introdução o ajude a começar a usar o módulo ``pygame.sprite``.
Lembre-se, a documentação de referência é a melhor referência sobre como o módulo
funciona. Há várias coisas que você pode fazer com ``Sprites`` e ``Groups`` que
eu nem mesmo toquei, mas este tutorial deve ajudar a orientar você. No entanto, a melhor
maneira de aprender é a prática. Se você tiver uma pergunta sobre o módulo
sprite, não hesite em perguntar em nossos foruns.

Bom jogo!
