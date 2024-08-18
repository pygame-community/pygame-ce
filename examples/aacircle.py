#!/usr/bin/env python

"""Proof of concept gfxdraw example"""

import pygame
import pygame.gfxdraw


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    screen.fill((255, 0, 0))
    s = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    pygame.draw.line(s, (0, 0, 0), (250, 250), (250 + 200, 250))

    width = 1
    for a_radius in range(width):
        radius = 200
        pygame.gfxdraw.aacircle(s, 250, 250, radius - a_radius, (0, 0, 0))

    screen.blit(s, (0, 0))

    pygame.draw.circle(screen, "green", (50, 100), 10)
    pygame.draw.circle(screen, "black", (50, 100), 10, 1)

    running = True

    clock = pygame.Clock()

    while running:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
