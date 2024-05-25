====================================
Autor: Youngwook Kim (Coreano)
====================================

====================================
Contato: rumia0601@gmail.com
====================================

====================================
Entrada Básica
====================================

====================================
-Nova Entrada é um Novo Evento
====================================
Normalmente, aprendemos como produzir algo primeiro (pense em Hello World!), aprender como inserir algo é sempre a segunda etapa. Por quê? Porque a entrada não é um requisito para alguns programas, ao contrário da saída, que é um requisito para todos os programas. (Essa é a definição de programa. Mais do que ou igual a 0 de entrada, mais do que ou igual a 1 de saída.) No entanto, todo jogo precisa de entrada. É por isso que dizemos "Gosto de jogar jogos". Jogar significa mover uma parte do seu corpo (talvez seu dedo). De qualquer forma, vamos adicionar lógica de entrada para transformar este projeto em um jogo real.

.. image:: ../../../assets/Bagic-INPUT-sourcecode.png
   :class: inlined-right

.. code-block:: python
   :linenos:

   import sys, pygame
   pygame.init()

   size = width, height = 220, 140
   speed = [2, 2]
   black = 0, 0, 0

   screen = pygame.display.set_mode(size)

   ball = pygame.image.load("Bagic-INPUT-sourcecode.png")
   ballrect = ball.get_rect()

   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT: sys.exit()

       ballrect = ballrect.move(speed)
       if ballrect.left < 0 or ballrect.right > width:
           speed[0] = -speed[0]
       if ballrect.top < 0 or ballrect.bottom > height:
           speed[1] = -speed[1]

       screen.fill(black)
       screen.blit(ball, ballrect)
       pygame.display.flip()


.. image:: ../../../assets/Bagic-INPUT-resultscreen.png
   :class: inlined-right

.. code-block:: python
   :linenos:

   import sys, pygame
   pygame.init()

   size = width, height = 220, 140
   speed = [2, 2]
   black = 0, 0, 0

   screen = pygame.display.set_mode(size)

   ball = pygame.image.load("Bagic-INPUT-resultscreen.png")
   ballrect = ball.get_rect()

   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT: sys.exit()

       ballrect = ballrect.move(speed)
       if ballrect.left < 0 or ballrect.right > width:
           speed[0] = -speed[0]
       if ballrect.top < 0 or ballrect.bottom > height:
           speed[1] = -speed[1]

       screen.fill(black)
       screen.blit(ball, ballrect)
       pygame.display.flip()


(Código Fonte para o Projeto Controlling World e sua tela de resultado)

(Não o código-fonte inteiro do Projeto Controlling World, mas parte)

(Controlling World! se move quando o jogador pressiona uma das quatro setas do teclado)


Existem 2 grandes diferenças em comparação com o projeto anterior. A primeira grande diferença é a linha #5, que adiciona a verificação se o evento ``KEYDOWN`` é acionado ou não. Outras linhas apenas mudam o algoritmo anterior para agir de maneira diferente. Sabemos que o mesmo comando pode fazer uma grande diferença em todo o programa quando é executado antes ou depois da Declaração de Evento. Preste atenção que o processo de alteração de localização aparece após a Declaração de Evento. (**Atualização após configuração**. Essa é a segunda grande diferença). A variável ``event.key`` significa a tecla mais recentemente pressionada no teclado. Olhe para o nome específico da tecla. K_UP, K_LEFT, K_DOWN, K_RIGHT. Série **K_ muito intuitiva**. (Dado por pygame.locals que adicionamos ao Header) Além disso, existem outras teclas chamadas K_8, K_a, K_L, K_LCTRL, K_DELETE, ou K_F4. Podemos entender o significado dessas teclas sem explicação adicional. A lista completa de teclas pode ser encontrada em `https://pyga.me/docs/ref/key.html#pygame.key.name`.

Observe que KEYDOWN significa "esta tecla não foi pressionada antes, mas **agora está pressionada**" e o significado de **"manter pressionado" não está incluído** aqui. No caso de manter pressionado, um novo tratamento de evento sobre ``KEYUP`` (significa "esta tecla foi pressionada antes, mas agora não está pressionada") é necessário com algum processamento (que precisa de variável e algoritmo extras). Isso será mencionado na parte avançada.

Adicionar entrada foi fácil porque é apenas adicionar uma fase if com um certo parâmetro de evento. Agora, o projeto do jogo está feito porque o projeto tem saída, processo e entrada passo a passo! Sério? Não. Este projeto não pode ser chamado de jogo porque não há **interação** entre pelo menos dois **objetos de jogo**, nenhuma **regra** para jogar (nem restrições (ex. HP, tempo) nem pontuação). Principalmente, não **divertido** (sem motivação, sem variedade de entrada e saída, sem conteúdo atraente) Primeiramente, precisamos aprender mais sobre entrada avançada (por exemplo, manipulação do status do mouse), processo (por exemplo, ideia para funcionalização) e saída (por exemplo, imprimir imagem/som ou visualizar dados internos) para florescer a interface/sistema do jogo. Não fique no nível de imprimir texto constante ou inserir uma tecla pressionada única. Claro, as experiências deste nível são realmente úteis para o nível avançado. Então, vamos para o nível avançado!

<Reference Code> ::

    import pygame, sys
    from pygame.locals import*

    white = (255,255,255)
    red = (255,0,0)
    green = (0,255,0)
    pygame.init()
    pygame.display.set_caption("Controlling World Project") 
    myScreen = pygame.display.set_mode((640, 480))
    myTextFont = pygame.font.Font("HoonWhitecatR.ttf", 32)
    myText = myTextFont.render("Controlling World!", True, red, green) 
    myTextArea = myText.get_rect()
    myTextArea.center = (320, 240)
    fpsClock = pygame.time.Clock()
    x = 0
    y = 0
    moveRight = 0 #1
    moveDown = 0 #2

    while True:
        moveRight = 0 #3
        moveDown = 0 #4
        myTextArea.center = (320 + x, 240 + y)
        myScreen.fill(white)
        myScreen.blit(myText, myTextArea)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN: #5
                if event.key == K_UP:
                    moveDown = -1
                    moveRight = 0
                elif event.key == K_LEFT:
                    moveDown = 0
                    moveRight = -1
                elif event.key == K_DOWN:
                    moveDown = 1
                    moveRight = 0
                elif event.key == K_RIGHT:
                    moveDown = 0
                    moveRight = 1
                
        if(moveRight == 1): #6
            x = x + 10
        elif(moveRight == -1): #7
            x = x - 10
        if(moveDown == 1): #8
            y = y + 10
        elif(moveDown == -1): #9
            y = y - 10

        pygame.display.update()
        fpsClock.tick(60)
