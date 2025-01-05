from sys import stdout
from pstats import Stats
from cProfile import Profile


import pygame

pygame.init()


def draw_line_short_inside():
    lines = [
        ((256, 256), (0, 0)),
        ((128, 256), (128, 0)),
        ((50, 256), (128, 0)),
        ((0, 240), (12, 56)),
        ((50, 40), (60, 11)),
    ]
    widths = [1, 2, 4, 6, 20]
    surf = pygame.Surface((256, 256), pygame.SRCALPHA, 32)
    surf.fill((255, 255, 255, 255))
    for iterations in range(0, 10000):
        for line in lines:
            for width in widths:
                pygame.draw.line(
                    surf, pygame.Color("red"), line[0], line[1], width=width
                )


def draw_line_long_inside():
    lines = [
        ((1256, 256), (0, 0)),
        ((1128, 256), (128, 0)),
        ((150, 1256), (128, 0)),
        ((0, 240), (1200, 56)),
        ((50, 40), (1060, 11)),
    ]
    widths = [1, 2, 4, 6, 20]
    surf = pygame.Surface((2048, 2048), pygame.SRCALPHA, 32)
    surf.fill((255, 255, 255, 255))
    for iterations in range(0, 10000):
        for line in lines:
            for width in widths:
                pygame.draw.line(
                    surf, pygame.Color("red"), line[0], line[1], width=width
                )


def draw_line_short_outside():
    lines = [
        ((256, 256), (0, 0)),
        ((128, 256), (128, 0)),
        ((50, 256), (128, 0)),
        ((0, 240), (12, 56)),
        ((50, 40), (80, 11)),
    ]
    widths = [1, 2, 4, 6, 20]
    surf = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
    surf.fill((255, 255, 255, 255))
    for iterations in range(0, 10000):
        for line in lines:
            for width in widths:
                pygame.draw.line(
                    surf, pygame.Color("red"), line[0], line[1], width=width
                )


def draw_line_long_outside():
    lines = [
        ((2256, 256), (0, 0)),
        ((2128, 256), (128, 0)),
        ((150, 4256), (128, 0)),
        ((0, 240), (2200, 56)),
        ((50, 40), (4060, 11)),
    ]
    widths = [1, 2, 4, 6, 20]
    surf = pygame.Surface((1024, 1024), pygame.SRCALPHA, 32)
    surf.fill((255, 255, 255, 255))
    for iterations in range(0, 10000):
        for line in lines:
            for width in widths:
                pygame.draw.line(
                    surf, pygame.Color("red"), line[0], line[1], width=width
                )


if __name__ == "__main__":
    print("Draw Line - short, inside surface")
    profiler = Profile()
    profiler.runcall(draw_line_short_inside)
    stats = Stats(profiler, stream=stdout)
    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats()

    print("\nDraw Line - long, inside surface")
    profiler = Profile()
    profiler.runcall(draw_line_long_inside)
    stats = Stats(profiler, stream=stdout)
    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats()

    print("\nDraw Line - short, edges outside surface")
    profiler = Profile()
    profiler.runcall(draw_line_short_outside)
    stats = Stats(profiler, stream=stdout)
    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats()

    print("\nDraw Line - long, edges a long way outside surface")
    profiler = Profile()
    profiler.runcall(draw_line_long_outside)
    stats = Stats(profiler, stream=stdout)
    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats()
