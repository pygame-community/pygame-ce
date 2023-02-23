#!/usr/bin/env python
""" pg.examples.stars

We are all in the gutter,
but some of us are looking at the stars.
                                        -- Oscar Wilde

A simple starfield example. Note you can move the center of
the starfield by leftclicking in the window. This example shows
the basics of creating a window, simple pixel plotting, and event management.
"""

import random
from typing import List

import pygame as pg


class Particle:
    def __init__(
        self,
        pos: List[int],
        vel: pg.Vector2,
    ):
        """
        Parameters:
            pos: Position of the particle
            vel: How far does the particle move (x, y) every frame
        """

        self.pos = pos
        self.vel = vel
        self.color_list = [
            (255, 210, 125),
            (255, 163, 113),
            (166, 168, 255),
            (255, 250, 134),
            (168, 123, 255),
        ]

    def draw(self, display: pg.Surface):
        """
        Draws the particle on a pygame.Surface
        Parameters:
            display: The surface the particle is drawn on
        """

        pg.draw.line(display, random.choice(self.color_list), self.pos, self.pos)

    def update(self):
        """
        Moves the particle
        """

        self.pos += self.vel


def create_particle(particle_list: List[Particle], pos: pg.Vector2):
    """
    Creates a new particle
    Parameters:
        particle_list: List of existing particles
        pos: The coordinates the new particle will be spawned on
    """

    particle_list.append(
        Particle(
            pos=pos.copy(),
            vel=pg.Vector2(random.uniform(-5, 5), random.uniform(-5, 5)),
        )
    )


def update_particles(particle_list: List[Particle], screen_rect: pg.Rect):
    """
    Updates the particles
    Parameters:
        particle_list: List of existing particles
        screen_rect: A pg.Rect that represents the screen
                (used to determine whether a particle is visible on the screen)
    """

    for particle in particle_list:
        if not screen_rect.collidepoint(particle.pos):
            particle_list.remove(particle)

        particle.update()


def draw_particles(particle_list: List[Particle], display: pg.Surface):
    """
    Draws the particles
    Parameters:
        particle_list: List of existing particles
        display: The surface the particle is drawn on
    """
    for particle in particle_list:
        particle.draw(display)


def main():
    """
    Contains the game variables and loop
    """
    screen = pg.display.set_mode((600, 500))
    clock = pg.time.Clock()
    pg.display.set_caption("Pygame Stars")
    particles = []
    # how many particles to spawn every frame
    particle_density = 10

    screen_rect = screen.get_rect()
    spawn_point = pg.Vector2(screen_rect.center)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                spawn_point = pg.Vector2(event.pos)

        screen.fill((20, 20, 40))
        for _ in range(particle_density):
            create_particle(particles, spawn_point)
        update_particles(particles, screen_rect)
        draw_particles(particles, screen)

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
