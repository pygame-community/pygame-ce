====================================
Autor: Youngwook Kim (Coreano)
====================================

====================================
Contato: rumia0601@gmail.com
====================================

====================================
Processo Básico
====================================

====================================
-Configuração para Animação
====================================
O projeto anterior parece uma única imagem em vez de um jogo. Isso porque não há entrada nem processo para controlar a saída. Claro, clicar no botão de saída na janela não conta, pois é apenas desligar o programa inteiro. Primeiro, faremos com que o texto "Hello World!" se mova automaticamente (e agora o projeto parecerá uma animação em vez de uma única imagem), o que significa adicionar a primeira lógica de processamento neste projeto. Como mover o texto? Sabemos que a localização do texto é inicializada na Declaração Inicial. Portanto, a localização do texto deve ser atualizada na Declaração Sempre, adicionando algumas variáveis para processar algo.

.. image:: Bagic-PROCESS-sourcecode.png
   :class: inlined-right

.. code-block:: python
   :linenos:

   import sys, pygame
   pygame.init()

   size = width, height = 220, 140
   speed = [2, 2]
   black = 0, 0, 0

   screen = pygame.display.set_mode(size)

   ball = pygame.image.load("Bagic-PROCESS-sourcecode.png")
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


.. image:: Bagic-PROCESS-resultscreen.png
   :class: inlined-right

.. code-block:: python
   :linenos:

   import sys, pygame
   pygame.init()

   size = width, height = 220, 140
   speed = [2, 2]
   black = 0, 0, 0

   screen = pygame.display.set_mode(size)

   ball = pygame.image.load("Bagic-PROCESS-resultscreen.png")
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


(Código Fonte para o Projeto Moving World e sua tela de resultado)

(Não o código-fonte inteiro do Projeto Moving World, mas parte)

(Moving World! se move automaticamente, assim como a bola Arkanoid ou o protetor de tela do DVD.)

As novas linhas #1 - #5 foram acrescentadas ao final da Declaração Inicial. Além disso, várias fases de if-else (#6 - #9) foram inseridas no início da Declaração Sempre, com a linha #11 no final das declarações sempre. Podemos entender o que os comandos de #2 - #10 fazem. Eles apenas alteram variáveis para a posição do "Moving World" quando a Declaração Sempre é iniciada. Mas há um problema. Quão rápido é o "Moving World"? É certo que o deslocamento do "Moving World" é sqrt(2) (equação pitagórica simples). Mas com que frequência o deslocamento do "Moving World" é alterado? Isso não pode ser determinado sem calcular a complexidade temporal da Declaração Sempre! (Porque depende de com que frequência a Declaração Sempre é iniciada) E a complexidade temporal será diferente de computador para computador, então não pode ser fixada.

Precisamos adicionar a noção de **velocidade fixa** a este projeto. Como? Olhe para #1 e #11. Há ``pygame.time.Clock()`` na Declaração Inicial e ``tick(60)`` na Declaração Sempre. 60 significa FPS (quadros por segundo). Sabemos que FPS significa com que frequência o display é alterado em 1 segundo. Qual função significa mudar (= atualizar) o display no pygame? Isso mesmo. A função Pygame.display.update(). Portanto, FPS significa com que frequência a Declaração Sempre é executada em 1 segundo. Porque há 1 função Pygame.display.update() em 1 declaração sempre. (Portanto, FPS significa **atraso seletivo** de acordo com a velocidade de processamento atual do programa, **não aceleração seletiva**, então o FPS não pode funcionar se o FPS for muito alto.) Se deixarmos o fps (= **tempo**) ser fixo neste projeto, podemos alterar a **velocidade** de certo objeto do jogo encontrando um valor apropriado para o **deslocamento**. pygame.time.Clock() é necessário para fixar a velocidade do projeto antes de o jogo começar. Observe que a função tick deve ser chamada quando Pygame.display.update() é chamada. Porque tick conta o número de funções de atualização. É uma das exceções à função que pode ser executada após Pygame.display.update().

Ok, aprendemos que "Fixar o tempo" é necessário quando o ecrã é atualizado. Cada ecrã de jogo dinâmico é alterado frequentemente a menos que seja um jogo estático. Portanto, temos que saber disso. No entanto, este projeto não parece um jogo porque seu resultado pode ser facilmente antecipado (não há entrada para mudar o resultado). Agora, a lógica de entrada será inserida.

<Código de Referência> ::

    import pygame, sys
    from pygame.locals import*

    white = (255,255,255)
    red = (255,0,0)
    green = (0,255,0)
    pygame.init()
    pygame.display.set_caption("Moving World Project") 
    myScreen = pygame.display.set_mode((640, 480))
    myTextFont = pygame.font.Font("HoonWhitecatR.ttf", 32)
    myText = myTextFont.render("Moving World!", True, red, green) 
    myTextArea = myText.get_rect()
    myTextArea.center = (320, 240)
    fpsClock = pygame.time.Clock() #1
    x = 0 #2
    y = 0 #3
    moveRight = 1 #4
    moveUp= 1 #5

    while True:
        if (moveRight == 1): #6
            x = x + 1
            if (x >= 320 - 75):
                moveRight = 0
        elif (moveRight == 0): #7
            x = x - 1
            if (x <= -320 + 75):
                moveRight = 1

        if (moveUp == 1): #8
            y = y + 1
            if (y >= 240 - 15):
                moveUp = 0
        elif (moveUp == 0): #9
            y = y - 1
            if (y <= -240 + 15):
                moveUp = 1

    myTextArea.center = (320 + x, 240 + y) #10
    
    myScreen.fill(white)
    myScreen.blit(myText, myTextArea)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(60) #11
