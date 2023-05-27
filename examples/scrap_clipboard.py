#!/usr/bin/env python
""" pygame.examples.scrap_clipboard

Demonstrates the clipboard capabilities of pygame.

Copy/paste!


Keyboard Controls
-----------------
    v - View the current clipboard data.
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

    instruction = "Keyboard Controls:\nV - View the current clipboard data.\nC - Copy some text into the clipboard.\nEscape - Quit"
    text = font.render(instruction, True, "white")
    screen.blit(text, (0, 0))

    text = font.render(
        f"Text on the clipboard:\n{clipboard_text}", True, "white", None, width - 20
    )
    screen.blit(text, (0, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                # Look for any text data in the clipboard.
                print("Looking for text in the clipboard.")
                if pygame.scrap.has_text():
                    print("Text found in the clipboard.")
                    clipboard_text = pygame.scrap.get_text()
                else:
                    print("No text in the clipboard.")

            elif event.key == pygame.K_c:
                # put some text into the clipboard.
                print("Putting text into the clipboard.")

                pygame.scrap.put_text(
                    "Hello World! This is some text from the pygame scrap example.",
                )

            elif event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()
        clock.tick(60)
pygame.quit()
