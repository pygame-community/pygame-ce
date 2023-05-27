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


def render_instructions():
    text = font.render("Press 'v' to view the clipboard", True, "white")
    screen.blit(text, (10, 10))

    text = font.render("Press 'c' to copy some text to the clipboard", True, "white")
    screen.blit(text, (10, 30))

    text = font.render("Press 'escape' to quit", True, "white")
    screen.blit(text, (10, 50))


pygame.init()
pygame.display.set_caption("Clipboard Example")
screen = pygame.display.set_mode((960, 540))
clock = pygame.Clock()
font = pygame.Font(None, 30)


clipboard_text = ""
running = True

while running:
    screen.fill("black")

    render_instructions()

    text = "Text on the clipboard:"
    text = font.render(text, True, "white")
    screen.blit(text, (10, 80))

    text = font.render(clipboard_text, True, "white", None, 790)
    screen.blit(text, (10, 110))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                # Look for any text data in the clipboard.
                print("Looking for text data in the clipboard..")

                if pygame.scrap.has_text():
                    print("Text found:")
                    text = pygame.scrap.get_text()
                    print(text)
                    clipboard_text = text

                else:
                    print("No text data in the clipboard.")
                pass

            elif event.key == pygame.K_c:
                # put some text into the clipboard.
                print("Putting some text into the clipboard")
                pygame.scrap.put_text(
                    "Hello World! This is some text from the pygame scrap example.",
                )
                clipboard_text = pygame.scrap.get_text()

            elif event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()
        clock.tick(60)
pygame.quit()
