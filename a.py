import numpy
import pygame
import random

from statistics import median
from timeit import timeit

def foo():

    c = pygame.math.invlerp(238782374, 34729374275, 0.3478098)

t = [timeit(foo, number=500_000) for _ in range(50)]
print(median(t))

print(pygame.math.remap(0, 100, 0, 200, 50))