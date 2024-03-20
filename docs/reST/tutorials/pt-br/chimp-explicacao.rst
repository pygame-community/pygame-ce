.. TUTORIAL: Descrições Linha por Linha do Exemplo do Chimp

.. include:: ../../common.txt

**********************************************************
  Tutoriais do Pygame - Exemplo do Chimp Linha por Linha
**********************************************************

Linha por Linha do Chimp
========================

.. rst-class:: docinfo

:Author: Pete Shinners
:Contact: pete@shinners.org

.. toctree::
   :hidden:

   ../chimp.py


Introdução
----------

Nos exemplos do *pygame*, há um exemplo simples chamado "chimp".
Este exemplo simula um macaco que pode ser socado movendo-se pela tela com
promessas de riqueza e recompensa. O exemplo em si é muito simples e um
pouco carente de código de verificação de erros. Este programa de exemplo demonstra muitas das
capacidades do pygame, como criar uma janela, carregar imagens e sons,
renderizar texto e manipulação básica de eventos e mouse.

O programa e as imagens podem ser encontrados na distribuição padrão
do pygame. Você pode executá-lo digitando `python -m pygame.examples.chimp` no
seu terminal.

Este tutorial passará pelo código bloco a bloco, explicando como
o código funciona. Também haverá menção de como o código poderia ser melhorado
e como a verificação de erros poderia ajudar.

Este é um excelente tutorial para pessoas que estão dando a primeira olhada no
código do *pygame*. Uma vez que o *pygame* estiver totalmente instalado, você pode encontrar
e executar a demonstração do chimp por conta própria no diretório de exemplos.

.. container:: fullwidth leading trailing

   .. rst-class:: small-heading

   (não, isso não é um anúncio de banner, é a captura de tela)

   .. image:: ../assets/chimpshot.gif
      :alt: banner do jogo do macaco

   :doc:`Código Fonte Completo <../chimp.py>`


Importar Módulos
----------------

Este é o código que importa todos os módulos necessários para o programa.
Ele também verifica a disponibilidade de alguns módulos opcionais do pygame. ::

    # Importar Módulos
    import os
    import pygame

    if not pygame.font:
        print("Aviso, fontes desativadas")
    if not pygame.mixer:
        print("Aviso, som desativado")

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, "data")


Primeiro, importamos o módulo padrão "os" do Python. Isso permite
fazer coisas como criar caminhos de arquivo independentes de plataforma.

Na próxima linha, importamos o pacote pygame.

Alguns módulos do pygame são opcionais e, se não forem encontrados,
avaliam como ``False``. Por causa disso, decidimos imprimir
uma mensagem de aviso se os módulos :mod:`font<pygame.font>` ou
:mod:`mixer <pygame.mixer>` no pygame não estiverem disponíveis.
(Embora eles só sejam indisponíveis em situações muito incomuns).

Por fim, preparamos dois caminhos para o resto do código usar.
``main_dir`` usa o módulo `os.path` e a variável `__file__` fornecida
pelo Python para localizar o arquivo python do jogo e extrair a pasta dele.
Em seguida, preparamos a variável ``data_dir`` para dizer às
funções de carregamento exatamente onde procurar.


Carregar Recursos
-----------------

Aqui temos duas funções que podemos usar para carregar imagens e sons. Vamos
analisar cada função individualmente nesta seção. ::

    def load_image(name, colorkey=None, scale=1):
        fullname = os.path.join(data_dir, name)
        image = pygame.image.load(fullname)

        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pygame.transform.scale(image, size)

        image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image, image.get_rect()


Esta função recebe o nome de uma imagem para carregar. Ela também
aceita opcionalmente um argumento que pode ser usado para definir uma tecla de cor para a imagem, e um argumento
para dimensionar a imagem. Uma tecla de cor é usada em gráficos para representar uma cor da
imagem que é transparente.

A primeira coisa que esta função faz é criar um caminho completo para o arquivo.
Neste exemplo, todos os recursos estão em um subdiretório "data". Usando
a função `os.path.join`, será criado um caminho que funciona para qualquer
plataforma na qual o jogo está sendo executado.

Em seguida, carregamos a imagem usando a função :func:`pygame.image.load`.
Após o carregamento da imagem, fazemos uma chamada importante
para a função `convert()`. Isso cria uma nova cópia de uma Surface e converte
seu formato de cor e profundidade para coincidir com o display. Isso significa que o blit
da imagem na tela acontecerá o mais rápido possível.

Em seguida, redimensionamos a imagem, usando a função :func:`pygame.transform.scale`.
Esta função recebe uma Surface e o tamanho para o qual ela deve ser redimensionada. Para escalar
por um escalar, podemos obter o tamanho e escalar o x e y pelo escalar.

Por último, configuramos a tecla de cor para a imagem. Se o usuário forneceu um argumento
para a tecla de cor, usamos esse valor como a tecla de cor para a imagem.
Isso normalmente seria apenas um valor de cor RGB, como (255, 255, 255) para
branco. Você também pode passar um valor de -1 como a tecla de cor. Neste caso, o
a função procurará a cor no pixel superior esquerdo da imagem e usará
essa cor como a tecla de cor. ::

    def load_sound(name):
        class NoneSound:
            def play(self):
                pass

        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()

        fullname = os.path.join(data_dir, name)
        sound = pygame.mixer.Sound(fullname)

        return sound


A seguir, temos a função para carregar um arquivo de som. A primeira coisa que esta função
faz é verificar se o módulo :mod:`pygame.mixer` foi importado corretamente.
Se não, ela retorna uma instância pequena de uma classe que possui um método de reprodução de espaço reservado.
Isso será suficiente para que este jogo seja executado sem
nenhuma verificação adicional de erro.

Esta função é semelhante à função de carregamento de imagem, mas lida com alguns
problemas diferentes. Primeiro, criamos um caminho completo para o arquivo de som e
carregamos o arquivo de som. Em seguida, simplesmente retornamos o objeto Sound carregado.


Classes de Objetos do Jogo
--------------------------

Aqui criamos duas classes para representar os objetos em nosso jogo. Quase
toda a lógica do jogo está nessas duas classes. Vamos examiná-las uma a uma aqui. ::

    class Fist(pygame.sprite.Sprite):
        """move um punho cerrado na tela, seguindo o mouse"""

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)  # chama o inicializador de Sprite
            self.image, self.rect = load_image("fist.png", -1)
            self.fist_offset = (-235, -80)
            self.punching = False

        def update(self):
            """move o punho com base na posição do mouse"""
            pos = pygame.mouse.get_pos()
            self.rect.topleft = pos
            self.rect.move_ip(self.fist_offset)
            if self.punching:
                self.rect.move_ip(15, 25)

        def punch(self, target):
            """retorna verdadeiro se o punho colidir com o alvo"""
            if not self.punching:
                self.punching = True
                hitbox = self.rect.inflate(-5, -5)
                return hitbox.colliderect(target.rect)

        def unpunch(self):
            """chamado para puxar o punho de volta"""
            self.punching = False


Aqui criamos uma classe para representar o punho do jogador. Ela é derivada de
a classe `Sprite` incluída no módulo :mod:`pygame.sprite`. A função `__init__`
é chamada quando novas instâncias dessa classe são criadas. A primeira coisa
que fazemos é garantir que chamemos a função `__init__` de nossa classe base. Isso
permite que a função `__init__` do Sprite prepare nosso objeto para ser usado como um
sprite. Este jogo usa uma das classes de desenho de sprite do tipo Group. Essas classes
podem desenhar sprites que têm um atributo "imagem" e "rect". Simplesmente alterando
esses dois atributos, o renderizador desenhará a imagem atual na posição atual.

Todos os sprites têm um método `update()`. Esta função é geralmente chamada
uma vez por quadro. É aqui que você deve colocar o código que move e atualiza
as variáveis para o sprite. O método `update()` para o punho move o
punho para a localização do ponteiro do mouse. Também desloca ligeiramente a posição do punho
se o punho estiver no estado de "soco".

As duas funções seguintes, `punch()` e `unpunch()`, mudam o estado de "soco"
para o punho. O método `punch()` também retorna um valor verdadeiro se o punho
colidir com o sprite de destino. ::

    class Chimp(pygame.sprite.Sprite):
        """move um macaco pela tela. Ele pode girar o
        macaco quando é socado."""

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)  # chama o inicializador de Sprite
            self.image, self.rect = load_image("chimp.png", -1, 4)
            screen = pygame.display.get_surface()
            self.area = screen.get_rect()
            self.rect.topleft = 10, 90
            self.move = 18
            self.dizzy = False

        def update(self):
            """caminhe ou gire, dependendo do estado do macaco"""
            if self.dizzy:
                self._spin()
            else:
                self._walk()

        def _walk(self):
            """movimente o macaco pela tela e gire nas extremidades"""
            newpos = self.rect.move((self.move, 0))
            if not self.area.contains(newpos):
                if self.rect.left < self.area.left or self.rect.right > self.area.right:
                    self.move = -self.move
                    newpos = self.rect.move((self.move, 0))
                    self.image = pygame.transform.flip(self.image, True, False)
            self.rect = newpos

        def _spin(self):
            """gire a imagem do macaco"""
            center = self.rect.center
            self.dizzy = self.dizzy + 12
            if self.dizzy >= 360:
                self.dizzy = False
                self.image = self.original
            else:
                rotate = pygame.transform.rotate
                self.image = rotate(self.original, self.dizzy)
            self.rect = self.image.get_rect(center=center)

        def punched(self):
            """isso fará com que o macaco comece a girar"""
            if not self.dizzy:
                self.dizzy = True
                self.original = self.image


A classe `Chimp` está fazendo um pouco mais de trabalho do que o punho, mas nada
mais complexo. Esta classe moverá o macaco para frente e para trás pela
tela. Quando o macaco é socado, ele girará para um efeito emocionante.
Esta classe também é derivada da classe base :class:`Sprite <pygame.sprite.Sprite>`,
e é inicializada da mesma forma que o punho. Ao inicializar, a classe
também define o atributo "área" como o tamanho da tela de exibição.

A função `update` para o macaco simplesmente olha para o estado atual de "dizzy",
que é verdadeiro quando o macaco está girando de um soco. Ela chama qualquer
o método `_spin` ou `_walk`. Essas funções têm um sublinhado como prefixo.
Esta é apenas uma convenção padrão do Python que sugere que esses métodos devem
ser usados apenas pela classe `Chimp`. Poderíamos ir tão longe a ponto de dar a eles dois
sublinhados, o que diria ao Python para realmente tentar torná-los métodos privados,
mas não precisamos dessa proteção. :)

O método `_walk` cria uma nova posição para o macaco, movendo o retângulo atual
por um deslocamento fornecido. Se esta nova posição cruzar fora da área de exibição
da tela, ela inverte o deslocamento de movimento. Ele também espelha
a imagem usando a função :func:`pygame.transform.flip`. Este é um efeito bruto
que faz o macaco parecer que está virando na direção em que está se movendo.

O método `_spin` é chamado quando o macaco está atualmente "dizzy". O dizzy
atributo é usado para armazenar a quantidade atual de rotação. Quando o macaco
girou completamente (360 graus), ele redefine a imagem do macaco
de volta à versão original, não girada. Antes de chamar o
:func:`pygame.transform.rotate`, você verá que o código faz uma referência local
à função simplesmente chamada "rotate". Não há necessidade de fazer isso
para este exemplo, é feito aqui apenas para manter o comprimento da linha seguinte um
pouco mais curto. Observe que ao chamar a função `rotate`, estamos sempre
rotacionando a partir da imagem original do macaco. Ao girar, há uma ligeira perda
de qualidade. Girar repetidamente a mesma imagem e a qualidade pioraria
cada vez. Além disso, ao girar uma imagem, o tamanho da imagem realmente
mudará. Isso ocorre porque os cantos da imagem serão girados para fora, tornando
a imagem maior. Certificamo-nos de que o centro da nova imagem corresponda ao centro
da imagem antiga, para que ela gire sem se mover.

O último método é `punched()`, que diz ao sprite para entrar no seu estado "dizzy".
Isso fará com que a imagem comece a girar. Também faz uma cópia
da imagem atual chamada "original".


Inicializar Tudo
----------------

Antes de podermos fazer muita coisa com o pygame, precisamos garantir que seus módulos
estejam inicializados. Neste caso, também abrimos uma janela gráfica simples.
Agora estamos na função `main()` do programa, que realmente executa tudo. ::

    pygame.init()
    screen = pygame.display.set_mode((1280, 480), pygame.SCALED)
    pygame.display.set_caption("Monkey Fever")
    pygame.mouse.set_visible(False)

A primeira linha para inicializar o *pygame* cuida de um pouco de
trabalho para nós. Ele verifica os módulos do *pygame* importados e tenta
inicializar cada um deles. É possível voltar e verificar se módulos
não foram inicializados corretamente, mas não nos incomodaremos aqui. Também é possível
ter mais controle e inicializar cada módulo específico manualmente. Isso
tipo de controle geralmente não é necessário, mas está disponível se você desejar.

Em seguida, configuramos o modo de exibição dos gráficos. Observe que o módulo :mod:`pygame.display`
é usado para controlar todas as configurações de exibição. Neste caso, estamos
pedindo uma janela de 1280 por 480, com a flag de exibição ``SCALED``.
Isso dimensiona automaticamente a janela para exibições muito maiores que a
janela.

Por último, definimos o título da janela e desligamos o cursor do mouse para nossa
janela. Normalmente, o cursor é visível por padrão, então não há necessidade
realmente definir o estado, a menos que queiramos escondê-lo.


Criar o Plano de Fundo
---------------------

Nosso programa terá uma mensagem de texto no plano de fundo. Seria
bom criar uma única superfície para representar o plano de fundo e
usar repetidamente isso. O primeiro passo é criar a superfície. ::

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

Isso cria uma nova superfície para nós que é do mesmo tamanho da janela de exibição.
Observe a chamada extra para `convert()` após a criação da superfície. O
convert sem argumentos garantirá que nosso plano de fundo seja do mesmo formato
que a janela de exibição, o que nos dará os resultados mais rápidos.

Também preenchemos todo o fundo com uma determinada cor verde. A função fill()
normalmente leva uma tripla RGB como argumento, mas suporta muitos
formatos de entrada. Consulte o :mod:`pygame.Color` para todos os formatos de cor.


Colocar Texto no Plano de Fundo, Centralizado
--------------------------------------------

Agora que temos uma superfície de fundo, vamos renderizar o texto nele. Nós
só fazemos isso se virmos que o módulo :mod:`pygame.font` foi importado corretamente.
Se não, apenas pulamos esta seção. ::

    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("Bata no Macaco e Ganhe $$$", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)

Como você vê, há alguns passos para fazer isso. Primeiro nós
devemos criar o objeto de fonte e renderizá-lo em uma nova superfície. Nós então encontramos
o centro dessa nova superfície e colamos (paste) no fundo.

A fonte é criada com o construtor `Font()` do módulo `font`. Normalmente
você passará o nome de um arquivo de fonte TrueType para esta função, mas nós
também podemos passar `None`, que usará uma fonte padrão. O construtor `Font`
também precisa saber o tamanho da fonte que queremos criar.

Em seguida, renderizamos essa fonte em uma nova superfície. A função `render`
cria uma nova superfície que é do tamanho apropriado para nosso texto. Neste caso,
também estamos dizendo para renderizar texto antialiasing (para uma aparência suave)
e usar uma cor cinza escura.

Em seguida, precisamos encontrar a posição centralizada do texto em nossa exibição.
Criamos um objeto "Rect" apropriado chamando `text.get_rect()` e modificamos-o para
ter a posição certa. Finalmente, colamos a imagem do texto no fundo.

Se o módulo `pygame.font` não foi importado corretamente, simplesmente pulamos
esta seção, pois ela é opcional.


Configurar os Grupos de Sprites
------------------------

Vamos criar alguns grupos de sprites para tornar a manipulação dos objetos do jogo mais fácil.
Temos um grupo para o punho e um grupo para o macaco. ::

    allsprites = pygame.sprite.RenderPlain((fist, chimp))
    fists = pygame.sprite.RenderPlain()

A função `RenderPlain` retorna um grupo de sprites que é apenas isso - uma coleção de sprites.
Este tipo de grupo é o mais simples disponível e é mais do que suficiente para
a maioria dos jogos. Em geral, você deseja ter tantos grupos quanto tipos diferentes
de objetos diferentes que você deseja desenhar. Isso permite que você desenhe todos os
objetos de um tipo em um passo, sem ter que se preocupar com a ordem.

O código acima cria dois grupos, `allsprites` e `fists`. `Allsprites`
é uma coleção de todos os sprites que precisamos desenhar. O grupo `fists`
contém apenas os punhos. Isso permite que tenhamos um grupo que contém apenas
o objeto que pode realmente se mover pela tela, e outro que contém todos os objetos
que devem ser desenhados, mas não movidos.


O Laço Principal
----------------

Agora que tudo está configurado, precisamos entrar no nosso loop principal do jogo.
Este é o código que executará o tempo todo. ::

    while True:
        clock.tick(40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                fists.add(Fist())
                allsprites.add(fists)

        allsprites.update()

        for fist in fists:
            chimp_punched = fist.punch(chimp)
            if chimp_punched:
                punch_sound.play()
                chimp.punched()

        for fist in fists:
            if fist.rect.left > screen.get_width():
                fist.unpunch()
                fists.remove(fist)

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

Isso é tudo que precisamos fazer para o nosso programa. O primeiro
loop `for` é responsável por pegar qualquer evento que aconteceu.
Atualmente, só verificamos se o botão do mouse foi pressionado. Se for, adicionamos
um novo punho ao grupo `fists`. Se fossemos construir este código para
um jogo mais complexo, poderíamos usar um mapeamento de eventos para funções
como fizemos com o tutorial de teclas.

O próximo bloco de código atualiza todos os sprites. Isso geralmente é chamado
a cada quadro, e isso é o que faz com que todos os sprites movam
suas posições, façam rotações e assim por diante. É importante chamar isso
antes de qualquer lógica do jogo para garantir que os sprites estejam em suas
posições corretas quando precisarmos deles.

O próximo bloco de código é onde todo o trabalho de jogo acontece. Nós
verificamos cada soco para ver se ele colide com o macaco. Se o
socar, reproduzimos um som de soco e definimos o estado "dizzy" do macaco.

Em seguida, passamos por todos os socos e removemos qualquer soco que tenha ido
muito longe. Isso evita que os socos continuem indefinidamente fora da tela.

Finalmente, desenhamos o fundo e, em seguida, desenhamos todos os sprites em
suas posições atuais. A função `pygame.display.flip()` atualiza a tela
para exibir nossa nova imagem. Este é um método mais eficiente do que usar
`pygame.display.update()` para atualizar apenas partes da tela.

Este ciclo continuará até que um evento `QUIT` ocorra, como fechar a janela.
Nesse ponto, o programa terminará. Este é o fim do nosso tutorial.
Espero que tenha ajudado você a entender como fazer jogos básicos com o *pygame*!
