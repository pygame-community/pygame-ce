#!/usr/bin/env python
""" pygame.examples.prevent_display_stretching

Prevent display stretching on Windows.

On some computers, the display environment can be configured to stretch
all windows so that they will not appear too small on the screen for
the user. This configuration is especially common on high-DPI displays.
pygame-ce graphics appear distorted when automatically stretched by the
display environment. This script demonstrates a technique for preventing
this stretching and distortion.

Limitations:
This script makes an API call that is only available on Windows (versions
Vista and newer).

"""

# Ensure that the computer is running Windows Vista or newer
import os
import sys

# game constants
TEXTCOLOR = "green"
BACKGROUNDCOLOR = "black"
AXISCOLOR = "white"

if os.name != "nt" or sys.getwindowsversion()[0] < 6:
    raise NotImplementedError("this script requires Windows Vista or newer")

import pygame

import ctypes

# Determine whether or not the user would like to prevent stretching
if os.path.basename(sys.executable) == "pythonw.exe":
    selection = "y"
else:
    selection = None
    while selection not in ("y", "n"):
        selection = input("Prevent stretching? (y/n): ").strip().lower()

if selection == "y":
    msg = "Stretching is prevented."
else:
    msg = "Stretching is not prevented."

# Prevent stretching
if selection == "y":
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

# Show screen
pygame.display.init()
RESOLUTION = (350, 350)
screen = pygame.display.set_mode(RESOLUTION)

# Render message onto a surface
pygame.font.init()
font = pygame.Font(None, 36)
msg_surf = font.render(msg, 1, TEXTCOLOR)
res_surf = font.render("Intended resolution: %ix%i" % RESOLUTION, 1, TEXTCOLOR)

# Control loop
running = True
clock = pygame.Clock()
counter = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUNDCOLOR)

    # Draw lines which will be blurry if the window is stretched
    # or clear if the window is not stretched.
    pygame.draw.line(screen, AXISCOLOR, (0, counter), (RESOLUTION[0] - 1, counter))
    pygame.draw.line(screen, AXISCOLOR, (counter, 0), (counter, RESOLUTION[1] - 1))

    # Blit message onto screen surface
    msg_blit_rect = screen.blit(msg_surf, (0, 0))
    screen.blit(res_surf, (0, msg_blit_rect.bottom))

    clock.tick(10)

    pygame.display.flip()

    counter += 1
    if counter == RESOLUTION[0]:
        counter = 0

pygame.quit()
