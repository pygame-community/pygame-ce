import pygame
import timeit
import random

surf = pygame.Surface((600, 600))
def draw():
    p1 = (random.randrange(0, 600), random.randrange(0, 600))
    p2 = (random.randrange(0, 600), random.randrange(0, 600))
    p3 = (random.randrange(0, 600), random.randrange(0, 600))
    pygame.draw.polygon(surf, pygame.Color("white"), [p1, p2, p3])

print(timeit.timeit(draw))