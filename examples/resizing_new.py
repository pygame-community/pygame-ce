#!/usr/bin/env python
import pygame

pygame.init()

RES = (160, 120)
FPS = 30
clock = pygame.Clock()

screen = pygame.display.set_mode(RES, pygame.RESIZABLE)
pygame.display._set_autoresize(False)

# MAIN LOOP

done = False

i = 0
j = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            done = True
        if event.type == pygame.QUIT:
            done = True
        # if event.type==pygame.WINDOWRESIZED:
        #    screen=pygame.display.get_surface()
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.get_surface()
    i += 1
    i = i % screen.get_width()
    j += i % 2
    j = j % screen.get_height()

    screen.fill((255, 0, 255))
    pygame.draw.circle(screen, (0, 0, 0), (100, 100), 20)
    pygame.draw.circle(screen, (0, 0, 200), (0, 0), 10)
    pygame.draw.circle(screen, (200, 0, 0), (160, 120), 30)
    pygame.draw.line(screen, (250, 250, 0), (0, 120), (160, 0))
    pygame.draw.circle(screen, (255, 255, 255), (i, j), 5)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
