====================================
Autor: Youngwook Kim (Coreano)
====================================

====================================
Contato: rumia0601@gmail.com
====================================

====================================
e mais alpha
====================================

Na verdade, tudo isso não parece um jogo. Agora, vamos inserir uma regra neste programa. Então. Isso se tornará um jogo. A regra é simples: contar vermelho ou preto de uma matriz 2D de 5x5 e escolher a cor que tem mais números! Se estiver correto, HP++, caso contrário, HP--. Em seguida, uma nova matriz será definida para a próxima pergunta! Muito simples, mas um jogo que pode ser feito neste tutorial. Primeiro, precisamos gerar uma matriz 2D e imprimi-la. Como? Aprendemos como imprimir dados inteiros (que são iguais a dados únicos (array 0D)) e dois botões (que são iguais a um único array (array 1D). O caso de uma matriz 2D precisa apenas de um passo a mais.

.. image:: AdvancedOutputAlpha1.gif
   :class: inlined-right

.. code-block:: python
   :linenos:

   import sys, pygame
   pygame.init()

   size = width, height = 320, 240
   speed = [2, 2]
   black = 0, 0, 0

   screen = pygame.display.set_mode(size)

   ball = pygame.image.load("AdvancedOutputAlpha1.gif")
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

.. image:: AdvancedOutputAlpha2.gif
   :class: inlined-right

.. code-block:: python
   :linenos:

   import sys, pygame
   pygame.init()

   size = width, height = 320, 240
   speed = [2, 2]
   black = 0, 0, 0

   screen = pygame.display.set_mode(size)

   ball = pygame.image.load("AdvancedOutputAlpha2.gif")
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

.. image:: AdvancedOutputAlpha3.gif
   :class: inlined-right

.. code-block:: python
   :linenos:

   import sys, pygame
   pygame.init()

   size = width, height = 320, 240
   speed = [2, 2]
   black = 0, 0, 0

   screen = pygame.display.set_mode(size)

   ball = pygame.image.load("AdvancedOutputAlpha3.gif")
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

A função generateboard retorna uma placa 2D gerada aleatoriamente com o número de blocos vermelhos e pretos. Desnecessário explicar. Além disso, a função printboard imprime a placa 2D pelo mesmo método que o array 1D. A cor de saída será alterada pelos dados de board[i][j] ser 1 ou não. Este tabuleiro é apenas para saída. O processamento da margem parece ser irritante porque temos que saber a localização exata calculando. Lembre-se de Prolog. A saída (resultado da execução) do Pygame é GUI, mas a entrada (codificação) do Pygame é CUI. Isso é Pygame.

Na verdade, há muitas ideias para melhorar este jogo. Que tal trocar o botão por um arquivo de imagem? Que tal adicionar efeito sonoro quando a escolha anterior estava correta ou não? Que tal definir um limite de tempo? Que tal adicionar efeito visual quando o jogador vencer (maxHP) ou não (minHP)? Que tal aumentar o tamanho do tabuleiro com outras cores? Que tal implementar o jogo Flood-it dado uma interface? Ainda há muitas opções porque este jogo é simples.

<Código de Referência> ::

    import pygame, sys, random
    from pygame.locals import*
    
    maxHP = 10 
    white = (255,255,255)
    gray = (127,127,127)
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    pygame.init()
    pygame.display.set_caption("Projeto Vermelho ou Preto")
    width = 640 
    height = 480
    myScreen = pygame.display.set_mode((width, height))
    myTextFont = pygame.font.Font("HoonWhitecatR.ttf", 32)
    myText = myTextFont.render((str(maxHP) + "/" + str(maxHP)), True, red, gray)
    myTextArea = myText.get_rect()
    myTextArea.center = (width/2, height/2)
    fpsClock = pygame.time.Clock()
    
    def main():
        HP = 5
        board, b_red, b_black = generateBoard(5,5) #1
        
        while True:
            myText = myTextFont.render((str(HP) + "/" + str(maxHP)), True, red, gray)
        
            myScreen.fill(gray)
    
            myScreen.blit(myText, myTextArea)
            drawHP(HP)
            drawButtons()
            drawBoard(board) #2
    
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        if HP != 10:
                            HP = HP + 1
                    elif event.key == K_DOWN:
                        if HP != 0:
                            HP = HP - 1
                elif event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    
                    if pygame.Rect(270, 425, 45, 45).collidepoint(x, y): #3
                        if b_red >= b_black:
                            if HP != 10:
                                HP = HP + 1
                            board, b_red, b_black = generateBoard(5,5)
                        elif b_red < b_black:
                            if HP != 0:
                                HP = HP - 1
                            board, b_red, b_black = generateBoard(5,5)
                            
                    elif pygame.Rect(325, 425, 45, 45).collidepoint(x, y): #4
                        if b_red <= b_black:
                            if HP != 10:
                                HP = HP + 1
                            board, b_red, b_black = generateBoard(5,5)
                        elif b_red > b_black:
                            if HP != 0:
                                HP = HP - 1
                            board, b_red, b_black = generateBoard(5,5)
        
            pygame.display.update()
            fpsClock.tick(60)
    
    def drawHP(HP):
        r = int((height - 40) / maxHP)
    
        pygame.draw.rect(myScreen, gray, (20, 20, 20, 20 + ((maxHP - 0.5) * r)))
    
        for i in range(maxHP):
            if HP >= (maxHP - i):
                pygame.draw.rect(myScreen, blue, (20, 20 + (i * r), 20, r))
            pygame.draw.rect(myScreen, white, (20, 20 + (i * r), 20, r), 1)
    
        return
    
    def drawButtons():
        r = 45
        r_margin = 10
        colors = [red, black]
        
        num = 2
        margin = int((width - ((r * num) + (r_margin * (num - 1)))) / 2)
        
        for i in range(0, num):
            left = margin + (i * r) + (i * r_margin)
            up = height - r - 10
            pygame.draw.rect(myScreen, colors[i], (left, up, r, r))
            pygame.draw.rect(myScreen, gray, (left + 2, up + 2, r - 4, r - 4), 2)    
    
    def generateBoard(width, height): #5
        board = []
        b_red = 0
        b_black = 0
        
        for x in range(width):
            column = []
            for y in range(height):
                column.append(random.randint(0, 1))
            board.append(column)
    
        for x in range(width):
            for y in range(height):
                if(board[x][y] == 1):
                     b_red = b_red + 1
                elif(board[x][y] == 0):
                    b_black = b_black + 1
            
        return board, b_red, b_black
    
    def drawBoard(board): #6
        r = 50
        b_width = 5
        b_height = 5
        l_margin = int((width - (b_width * r)) / 2)
        u_margin = int((height - (b_height * r)) / 2)
    
        for x in range(5):
            for y in range(5):
                left = x * r + l_margin
                up = y * r + u_margin
                if board[x][y] == 1:
                    color = red;
                elif board[x][y] == 0:
                    color = black
                pygame.draw.rect(myScreen, color, (left, up, r, r))
                
        left = l_margin
        up = u_margin
        pygame.draw.rect(myScreen, white, (left-1, up-1, r * 5 + 1, r * b_height + 1), 1)
    
    if __name__ == '__main__':
        main()
