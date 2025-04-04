#!/usr/bin/env python
"""pygame.examples.scaletest

Shows an interactive image scaler.

"""

import sys
import time

import pygame


def main(imagefile, convert_alpha=False, run_speed_test=False):
    """show an interactive image scaler

    Args:
        imagefile - name of source image (required)
        convert_alpha - use convert_alpha() on the surf (default False)
        run_speed_test - (default False)
    """

    # initialize display
    pygame.display.init()
    # load background image
    background = pygame.image.load(imagefile)

    if run_speed_test:
        if convert_alpha:
            # convert_alpha() requires the display mode to be set
            pygame.display.set_mode((1, 1))
            background = background.convert_alpha()

        speed_test(background)
        return

    # start FULLSCREEN mode
    # On Windows, the fullscreen mode doesn't work properly, to fix the problem,
    # add with it pygame.SCALED flag
    screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN | pygame.SCALED)
    if convert_alpha:
        background = background.convert_alpha()

    # turn off the mouse pointer
    pygame.mouse.set_visible(False)

    running = True
    cursize = [background.get_width(), background.get_height()]

    clock = pygame.Clock()

    # main loop
    while running:
        clock.tick(60)

        image = pygame.transform.smoothscale(background, cursize)
        imgpos = image.get_rect(centerx=512, centery=384)
        screen.fill((255, 255, 255))
        screen.blit(image, imgpos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP]:
            cursize[1] -= 2
            if cursize[1] < 1:
                cursize[1] = 1
        if pressed_keys[pygame.K_DOWN]:
            cursize[1] += 2
        if pressed_keys[pygame.K_LEFT]:
            cursize[0] -= 2
            if cursize[0] < 1:
                cursize[0] = 1
        if pressed_keys[pygame.K_RIGHT]:
            cursize[0] += 2
    pygame.quit()


def speed_test(image):
    print(f"\nImage Scaling Speed Test - Image Size {str(image.get_size())}\n")

    imgsize = [image.get_width(), image.get_height()]
    duration = 0.0
    for i in range(128):
        shrinkx = (imgsize[0] * i) // 128
        shrinky = (imgsize[1] * i) // 128
        start = time.time()
        tempimg = pygame.transform.smoothscale(image, (shrinkx, shrinky))
        duration += time.time() - start
        del tempimg

    print(f"Average transform.smoothscale shrink time: {duration / 128 * 1000:.4f} ms.")

    duration = 0.0
    for i in range(128):
        expandx = (imgsize[0] * (i + 129)) // 128
        expandy = (imgsize[1] * (i + 129)) // 128
        start = time.time()
        tempimg = pygame.transform.smoothscale(image, (expandx, expandy))
        duration += time.time() - start
        del tempimg

    print(f"Average transform.smoothscale expand time: {duration / 128 * 1000:.4f} ms.")

    duration = 0.0
    for i in range(128):
        shrinkx = (imgsize[0] * i) // 128
        shrinky = (imgsize[1] * i) // 128
        start = time.time()
        tempimg = pygame.transform.scale(image, (shrinkx, shrinky))
        duration += time.time() - start
        del tempimg

    print(f"Average transform.scale shrink time: {duration / 128 * 1000:.4f} ms.")

    duration = 0.0
    for i in range(128):
        expandx = (imgsize[0] * (i + 129)) // 128
        expandy = (imgsize[1] * (i + 129)) // 128
        start = time.time()
        tempimg = pygame.transform.scale(image, (expandx, expandy))
        duration += time.time() - start
        del tempimg

    print(f"Average transform.scale expand time: {duration / 128 * 1000:.4f} ms.")


if __name__ == "__main__":
    # check input parameters
    if len(sys.argv) < 2:
        print(f"\nUsage: {sys.argv[0]} imagefile [-t] [-convert_alpha]")
        print("    imagefile       image filename (required)")
        print("    -t              run speed test")
        print("    -convert_alpha  use convert_alpha() on the image's surface\n")
    else:
        main(
            sys.argv[1],
            convert_alpha="-convert_alpha" in sys.argv,
            run_speed_test="-t" in sys.argv,
        )
