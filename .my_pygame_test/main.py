import pygame
from pygame.geometry import Line

pygame.init()

window = pygame.display.set_mode((600, 600))

l = Line(10, 10, 200, 200)
p = (1, 1)

running = True
while running:

    window.fill((255, 255, 255))

    pygame.draw.line(window, (255, 0, 0), l.a, l.b, 5)
    
    pygame.draw.circle(window, (0, 255, 0), p, 5)
    pygame.draw.circle(window, (0, 255, 0), l.project(p, do_clamp=True), 5)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
