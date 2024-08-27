#!/usr/bin/env python
"""pygame.examples.dropfile

Drag and drop an image on here.

Uses these events:

* DROPBEGIN
* DROPCOMPLETE
* DROPTEXT
* DROPFILE
"""

import pygame

pygame.init()


def main():
    running = True
    screen_size = (640, 480)
    surf = pygame.display.set_mode(screen_size)
    font = pygame.font.SysFont("Arial", 24)
    font.align = pygame.FONT_CENTER
    clock = pygame.Clock()

    spr_file_text = font.render("Feed me some file or image!", True, (255, 255, 255))
    spr_file_text_rect = spr_file_text.get_rect()
    spr_file_text_rect.center = surf.get_rect().center

    spr_file_image = None
    spr_file_image_rect = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.DROPBEGIN:
                print(event)
                print("File drop begin!")
            elif event.type == pygame.DROPCOMPLETE:
                print(event)
                print("File drop complete!")
            elif event.type == pygame.DROPTEXT:
                print(event)
                spr_file_text = font.render(
                    event.text, True, (255, 255, 255), wraplength=screen_size[0] - 10
                )
                spr_file_text_rect = spr_file_text.get_rect()
                spr_file_text_rect.center = surf.get_rect().center
            elif event.type == pygame.DROPFILE:
                print(event)
                spr_file_text = font.render(
                    event.file, True, (255, 255, 255), None, screen_size[0] - 10
                )
                spr_file_text_rect = spr_file_text.get_rect()
                spr_file_text_rect.center = surf.get_rect().center

                # Try to open the file if it's an image
                filetype = event.file[-3:]
                if filetype in ["png", "bmp", "jpg"]:
                    spr_file_image = pygame.image.load(event.file).convert()
                    spr_file_image.set_alpha(127)
                    spr_file_image_rect = spr_file_image.get_rect()
                    spr_file_image_rect.center = surf.get_rect().center

        surf.fill((0, 0, 0))
        surf.blit(spr_file_text, spr_file_text_rect)
        if spr_file_image:
            surf.blit(spr_file_image, spr_file_image_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
