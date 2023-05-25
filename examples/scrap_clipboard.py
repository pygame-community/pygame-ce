#!/usr/bin/env python
""" pygame.examples.scrap_clipboard

Demonstrates the clipboard capabilities of pygame.

Copy/paste!


Keyboard Controls
-----------------
    v - View the current clipboard data.
    c - Copy some text into the clipboard.

"""


def usage():
    print("Press the 'v' key to view the current string in the clipboard")
    print("Press the 'c' key to put a string into the clipboard")
    print("Press the 'escape' key to quit")


usage()


def render_instructions():
    screen.fill((0, 0, 0))

    text = font.render("Press 'v' to view the clipboard", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    text = font.render(
        "Press 'c' to copy some text to the clipboard", True, (255, 255, 255)
    )
    screen.blit(text, (10, 30))

    text = font.render("Press 'escape' to quit", True, (255, 255, 255))
    screen.blit(text, (10, 50))


import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

pygame.font.init()
font = pygame.font.Font(None, 20)

# Initialize the scrap module and use the clipboard mode.
pygame.scrap.init()
pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

while running:
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
                else:
                    print("No text data in the clipboard.")
                pass

            elif event.key == pygame.K_c:
                # put some text into the clipboard.
                print("Putting some text into the clipboard")
                pygame.scrap.put_text(
                    "Hello World! This is some text from the pygame scrap example.",
                )

            elif event.key == pygame.K_ESCAPE:
                running = False

            else:
                usage()

        render_instructions()

        pygame.display.flip()
        clock.tick(30)
pygame.quit()
