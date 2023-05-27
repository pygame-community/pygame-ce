#!/usr/bin/env python
""" pygame.examples.scrap_clipboard

Demonstrates the clipboard capabilities of pygame.

Copy/paste!


Keyboard Controls
-----------------
    c - Copy some text into the clipboard.
"""


import pygame


pygame.init()
pygame.display.set_caption("Clipboard Example")
width, height = (960, 540)
screen = pygame.display.set_mode((width, height))
clock = pygame.Clock()
font = pygame.Font(None, 30)


clipboard_text = ""
running = True

while running:
    screen.fill("black")

    instruction = (
        "Keyboard Controls: \n c - Copy some text into the clipboard. \n escape - Quit"
    )
    text = font.render(instruction, True, "white")
    screen.blit(text, (0, 00))

    text = font.render("Text on the clipboard:", True, "white")
    screen.blit(text, (10, 100))

    text = font.render(clipboard_text, True, "white", None, width - 20)
    screen.blit(text, (10, 120))

    # First, check if there is any text data in the clipboard.
    if pygame.scrap.has_text():
        # If there is, get it and display it.
        clipboard_text = pygame.scrap.get_text()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                pygame.scrap.put_text(
                    "Hello World! This is some text from the pygame scrap example.",
                )

            elif event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()
        clock.tick(60)
pygame.quit()
