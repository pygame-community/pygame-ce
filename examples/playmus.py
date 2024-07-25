#!/usr/bin/env python
"""pygame.examples.playmus

A simple music player.

   Use pygame.mixer.music to play an audio file.

A window is created to handle keyboard events for playback commands.


Keyboard Controls
-----------------

space - play/pause toggle
r     - rewind
f     - fade out
q     - stop

"""

import sys

import pygame

pygame.init()


def write_lines(
    dest: pygame.Surface,
    text: str,
    font=pygame.Font(None, 30),
    color=(254, 231, 21, 255),
    starting_line=0,
):
    text_surface = font.render(text, True, color)

    y_offset = 0
    if starting_line >= 0:
        y_offset = font.get_height() * starting_line
    else:
        y_offset = dest.get_height() + starting_line * font.get_height()

    dest.fill(
        (16, 24, 32, 255),
        pygame.Rect((0, y_offset), (text_surface.get_width(), dest.get_width())),
    )
    dest.blit(text_surface, (16, y_offset))


def show_usage_message():
    print(
        "Usage: python playmus.py <file>\n"
        "       python -m pygame.examples.playmus <file>"
    )


def main(file_path):
    """Play an audio file with pygame.mixer.music"""

    screen = pygame.display.set_mode((600, 400))
    screen.fill((16, 24, 32, 255))

    write_lines(screen, "Loading ...", starting_line=-1)
    pygame.mixer.init(frequency=44100)
    pygame.mixer.music.load(file_path)

    pygame.display.set_caption(f"File : {file_path}")

    write_lines(
        screen,
        "Press 'q' or 'ESCAPE' or close this window to quit\n"
        "Press 'SPACE' to play / pause\n"
        "Press 'r' to rewind to the beginning (restart)\n"
        "Press 'f' to fade music out over 5 seconds",
        starting_line=1,
    )

    pygame.mixer.music.play()
    write_lines(screen, "Playing ...\n", starting_line=-1)

    running = True
    paused = False

    while running:
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_SPACE:
                    if paused:
                        pygame.mixer.music.unpause()
                        paused = False
                        write_lines(screen, "Playing ...", starting_line=-1)
                    else:
                        pygame.mixer.music.pause()
                        paused = True
                        write_lines(screen, "Paused ...", starting_line=-1)
                elif key == pygame.K_r:
                    if file_path[-3:].lower() in ("ogg", "mp3", "mod"):
                        status = "Rewound."
                        pygame.mixer.music.rewind()
                    else:
                        status = "Restarted."
                        pygame.mixer.music.play()
                    if paused:
                        pygame.mixer.music.pause()
                        write_lines(screen, status, starting_line=-1)
                elif key == pygame.K_f:
                    write_lines(screen, "Fading out ...", starting_line=-1)
                    pygame.mixer.music.fadeout(5000)
                    # when finished get_busy() will return False.
                elif key in [pygame.K_q, pygame.K_ESCAPE]:
                    paused = False
                    pygame.mixer.music.stop()
                    # get_busy() will now return False.
            elif event.type == pygame.QUIT:
                running = False

        if not pygame.mixer.music.get_busy() and not paused:
            running = False

    pygame.quit()


if __name__ == "__main__":
    # Check the only command line argument, a file path
    if len(sys.argv) != 2:
        show_usage_message()
    else:
        main(sys.argv[1])
