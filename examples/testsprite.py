#!/usr/bin/env python
"""pygame.examples.testsprite

Like the testsprite.c that comes with libsdl, this pygame version shows
lots of sprites moving around.

It is an abomination of ugly code, and mostly used for testing.


See pygame.examples.aliens for some prettier code.
"""

import os
import sys
from random import randint
from time import time

import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


# use this to use update rects or not.
#  If the screen is mostly full, then update rects are not useful.
update_rects = True
if "-update_rects" in sys.argv:
    update_rects = True
if "-noupdate_rects" in sys.argv:
    update_rects = False

use_static = False
if "-static" in sys.argv:
    use_static = True


use_layered_dirty = False
if "-layered_dirty" in sys.argv:
    update_rects = True
    use_layered_dirty = True


flags = 0
if "-flip" in sys.argv:
    flags ^= pygame.DOUBLEBUF

if "-fullscreen" in sys.argv:
    flags ^= pygame.FULLSCREEN

if "-sw" in sys.argv:
    flags ^= pygame.SWSURFACE

use_rle = True

if "-scaled" in sys.argv:
    flags ^= pygame.SCALED

screen_dims = [640, 480]

if "-height" in sys.argv:
    i = sys.argv.index("-height")
    screen_dims[1] = int(sys.argv[i + 1])

if "-width" in sys.argv:
    i = sys.argv.index("-width")
    screen_dims[0] = int(sys.argv[i + 1])

if "-alpha" in sys.argv:
    use_alpha = True
else:
    use_alpha = False

print(screen_dims)


class Thingy(pygame.sprite.DirtySprite):
    images = None

    def __init__(self):
        ##        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.DirtySprite.__init__(self)
        self.image = Thingy.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, screen_dims[0])
        self.rect.y = randint(0, screen_dims[1])
        # self.vel = [randint(-10, 10), randint(-10, 10)]
        self.vel = [randint(-1, 1), randint(-1, 1)]
        self.dirty = 2

    def update(self):
        for i in [0, 1]:
            nv = self.rect[i] + self.vel[i]
            if nv >= screen_dims[i] or nv < 0:
                self.vel[i] = -self.vel[i]
                nv = self.rect[i] + self.vel[i]
            self.rect[i] = nv


class Static(pygame.sprite.DirtySprite):
    images = None

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = Static.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, int(3 * screen_dims[0] / 4))
        self.rect.y = randint(0, int(3 * screen_dims[1] / 4))


def main(
    update_rects=True,
    use_static=False,
    use_layered_dirty=False,
    screen_dims=[640, 480],
    use_alpha=False,
    flags=0,
):
    """Show lots of sprites moving around

    Optional keyword arguments:
    update_rects - use the RenderUpdate sprite group class (default True)
    use_static - include non-moving images (default False)
    use_layered_dirty - Use the FastRenderGroup sprite group (default False)
    screen_dims - Pygame window dimensions (default [640, 480])
    use_alpha - use alpha blending (default False)
    flags - additional display mode flags (default no additional flags)

    """

    if use_layered_dirty:
        update_rects = True

    pygame.init()  # needed to initialise time module for get_ticks()
    pygame.display.init()

    # if "-fast" in sys.argv:

    screen = pygame.display.set_mode(screen_dims, flags, vsync="-vsync" in sys.argv)

    # this is mainly for GP2X, so it can quit.
    pygame.joystick.init()
    num_joysticks = pygame.joystick.get_count()
    if num_joysticks > 0:
        stick = pygame.joystick.Joystick(0)
        stick.init()  # now we will receive events for the joystick

    screen.fill([0, 0, 0])
    pygame.display.flip()
    sprite_surface = pygame.image.load(os.path.join(data_dir, "asprite.bmp"))
    sprite_surface2 = pygame.image.load(os.path.join(data_dir, "static.webp"))

    if use_rle:
        sprite_surface.set_colorkey(
            [0xFF, 0xFF, 0xFF], pygame.SRCCOLORKEY | pygame.RLEACCEL
        )
        sprite_surface2.set_colorkey(
            [0xFF, 0xFF, 0xFF], pygame.SRCCOLORKEY | pygame.RLEACCEL
        )
    else:
        sprite_surface.set_colorkey([0xFF, 0xFF, 0xFF], pygame.SRCCOLORKEY)
        sprite_surface2.set_colorkey([0xFF, 0xFF, 0xFF], pygame.SRCCOLORKEY)

    if use_alpha:
        sprite_surface = sprite_surface.convert_alpha()
        sprite_surface2 = sprite_surface2.convert_alpha()
    else:
        sprite_surface = sprite_surface.convert()
        sprite_surface2 = sprite_surface2.convert()

    Thingy.images = [sprite_surface]
    if use_static:
        Static.images = [sprite_surface2]

    if len(sys.argv) > 1:
        try:
            numsprites = int(sys.argv[-1])
        except Exception:
            numsprites = 100
    else:
        numsprites = 100
    sprites = None
    if use_layered_dirty:
        ##        sprites = pygame.sprite.FastRenderGroup()
        sprites = pygame.sprite.LayeredDirty()
    else:
        if update_rects:
            sprites = pygame.sprite.RenderUpdates()
        else:
            sprites = pygame.sprite.Group()

    for i in range(0, numsprites):
        if use_static and i % 2 == 0:
            sprites.add(Static())
        sprites.add(Thingy())

    frames = 0
    start = time()

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill([0, 0, 0])

    going = True
    while going:
        if not update_rects:
            screen.fill([0, 0, 0])

        ##        for sprite in sprites:
        ##            sprite.move()

        if update_rects:
            sprites.clear(screen, background)
        sprites.update()

        rects = sprites.draw(screen)
        if update_rects:
            pygame.display.update(rects)
        else:
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type in [
                pygame.QUIT,
                pygame.KEYDOWN,
                pygame.QUIT,
                pygame.JOYBUTTONDOWN,
            ]:
                going = False

        frames += 1
    end = time()
    print(f"FPS: {frames / (end - start):f}")
    pygame.quit()


if __name__ == "__main__":
    main(update_rects, use_static, use_layered_dirty, screen_dims, use_alpha, flags)
