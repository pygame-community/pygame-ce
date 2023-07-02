import pygame

try:
    p1 = pygame.PixelArray(pygame.Surface((0, 5)))[0]
except ValueError:
    print("test")
try:
    p2 = pygame.PixelArray(pygame.Surface((5, 0)))[0]
except ValueError:
    pass
