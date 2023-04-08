#!/usr/bin/env python
""" pygame.examples.blend_fill

BLEND_ing colors in different ways with Surface.fill().

Keyboard Controls:

* Press R, G, B to increase the color channel values,
* 1-9 to set the step range for the increment,
* A - ADD, S- SUB, M- MULT, - MIN, + MAX to change the blend modes

"""
import os
import pygame
from pygame import K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9


def usage():
    print("Press R, G, B to increase the color channel values,")
    print("1-9 to set the step range for the increment,")
    print("A - ADD, S- SUB, M- MULT, - MIN, + MAX")
    print("  to change the blend modes")


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


def main():
    color = [0, 0, 0]
    changed = False
    blendtype = 0
    step = 5

    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    screen.fill((100, 100, 100))

    image = pygame.image.load(os.path.join(data_dir, "liquid.bmp")).convert()
    blendimage = pygame.image.load(os.path.join(data_dir, "liquid.bmp")).convert()
    screen.blit(image, (10, 10))
    screen.blit(blendimage, (200, 10))

    pygame.display.flip()
    pygame.key.set_repeat(500, 30)
    usage()

    going = True
    while going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False

            if event.type == pygame.KEYDOWN:
                usage()

                if event.key == pygame.K_ESCAPE:
                    going = False

                if event.key == pygame.K_r:
                    color[0] += step
                    if color[0] > 255:
                        color[0] = 0
                    changed = True

                elif event.key == pygame.K_g:
                    color[1] += step
                    if color[1] > 255:
                        color[1] = 0
                    changed = True

                elif event.key == pygame.K_b:
                    color[2] += step
                    if color[2] > 255:
                        color[2] = 0
                    changed = True

                elif event.key == pygame.K_a:
                    blendtype = pygame.BLEND_ADD
                    changed = True
                elif event.key == pygame.K_s:
                    blendtype = pygame.BLEND_SUB
                    changed = True
                elif event.key == pygame.K_m:
                    blendtype = pygame.BLEND_MULT
                    changed = True
                elif event.key == pygame.K_PLUS:
                    blendtype = pygame.BLEND_MAX
                    changed = True
                elif event.key == pygame.K_MINUS:
                    blendtype = pygame.BLEND_MIN
                    changed = True

                elif event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9):
                    step = int(event.unicode)

            if changed:
                screen.fill((100, 100, 100))
                screen.blit(image, (10, 10))
                blendimage.blit(image, (0, 0))
                # blendimage.fill (color, (0, 0, 20, 20), blendtype)
                blendimage.fill(color, None, blendtype)
                screen.blit(blendimage, (200, 10))
                print(
                    f"Color: {tuple(color)}, Pixel (0,0): {[blendimage.get_at((0, 0))]}"
                )
                changed = False
                pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
