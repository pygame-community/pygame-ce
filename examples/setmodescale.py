#!/usr/bin/env python
""" pygame.examples.setmodescale

On high resolution displays(4k, 1080p) and tiny graphics games (640x480)
show up very small so that they are unplayable. SCALED scales up the window
for you. The game thinks it's a 640x480 window, but really it can be bigger.
Mouse events are scaled for you, so your game doesn't need to do it.

Passing SCALED to pygame.display.set_mode means the resolution depends
on desktop size and the graphics are scaled.
"""

import pygame
import sys

pygame.init()

RES = (160, 120)
FPS = 30
clock = pygame.Clock()

print("desktops", pygame.display.get_desktop_sizes())

do_vsync = bool("--vsync" in sys.argv)

if do_vsync:
    screen = pygame.display.set_mode(RES, pygame.SCALED | pygame.RESIZABLE, vsync=1)
else:
    screen = pygame.display.set_mode(RES, pygame.SCALED | pygame.RESIZABLE)

# MAIN LOOP

done = False

i = 0
j = 0

r_name, r_flags = pygame.display._get_renderer_info()
print("renderer:", r_name, "flags:", bin(r_flags))
for flag, name in [
    (1, "software"),
    (2, "accelerated"),
    (4, "VSync"),
    (8, "render to texture"),
]:
    if flag & r_flags:
        print(name)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            done = True
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            pygame.display.toggle_fullscreen()
    i += 1
    i = i % screen.get_width()
    j += i % 2
    j = j % screen.get_height()

    screen.fill((255, 0, 255))
    pygame.draw.circle(screen, (0, 0, 0), (100, 100), 20)
    pygame.draw.circle(screen, (0, 0, 200), (0, 0), 10)
    pygame.draw.circle(screen, (200, 0, 0), (160, 120), 30)
    if do_vsync:
        # vertical line that moves horizontally to make screen tearing obvious
        pygame.draw.line(screen, (250, 250, 0), (i, 0), (i, 120))
    else:
        pygame.draw.line(screen, (250, 250, 0), (0, 120), (160, 0))
    pygame.draw.circle(screen, (255, 255, 255), (i, j), 5)

    pygame.display.set_caption("FPS:" + str(clock.get_fps()))
    if do_vsync:
        pygame.display.flip()
        # FPS should be limited by vsync, so we tick really fast
        # we only need to have the clock tick to track FPS
        clock.tick()
    else:
        clock.tick(FPS)
        pygame.display.flip()

pygame.quit()
