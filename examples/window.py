#!/usr/bin/env python
""" pygame.examples.window

Demonstrates the new Window API, which can be used in place of
pygame.display.set_mode, providing more control and an object oriented
interface.
"""
import pygame

WIN_MOVE_SPEED = 25
WIN_GROW_SPEED = 15
COLOR_PROGRESSION = ["cadetblue2", "darkorange2", "lightslateblue", "seagreen"]
UNHOVERED_OPACITY = 0.8
SHOW_WINDOW = pygame.event.custom_type()

pygame.init()
pygame.key.set_repeat(500, 100)

main_window = pygame.Window("demo window", (500, 500), resizable=True)
main_surface = main_window.get_surface()
windows_and_surfaces = [(main_window, main_surface)]

instructions = """Welcome to the window demo!
Controls:
m.) maximize main window
n.) minimize main window
r.) restore main window 
    (from being minimized or maximized)
h.) hide main window for 1 second
s.) spawn a new window
arrow keys.) move window(s) around screen
escape.) destroy the most recently created window
1.) shrink all windows
2.) grow all windows
"""

font = pygame.font.SysFont("Arial", 24)
rendered_instructions = font.render(instructions, True, "black")

# Make sure instructions can be shown
main_window.minimum_size = rendered_instructions.get_size()

clock = pygame.Clock()
running = True

while running:
    for event in pygame.event.get():
        # If there are multiple windows, QUIT fires when the last one is destroyed
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.WINDOWCLOSE:
            index = [win_surface[0] for win_surface in windows_and_surfaces].index(
                event.window
            )
            del windows_and_surfaces[index]
            event.window.destroy()

        if event.type == pygame.WINDOWENTER:
            if event.window != main_window:
                try:
                    event.window.opacity = 1.0
                except pygame.error:
                    pass

        if event.type == pygame.WINDOWLEAVE:
            # Test not None because WINDOWLEAVE will trigger when a window
            # closes, can't set opacity of now-nonexistent Window.
            if event.window != main_window and event.window is not None:
                try:
                    event.window.opacity = UNHOVERED_OPACITY
                except pygame.error:
                    pass

        if event.type == SHOW_WINDOW:
            main_window.show()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                win, _ = windows_and_surfaces.pop()
                win.destroy()

                # Destroying the windows will not automatically do a QUIT on
                # last window, unlike closing the windows manually.
                if len(windows_and_surfaces) == 0:
                    pygame.event.post(pygame.Event(pygame.QUIT))

            if event.key == pygame.K_m:
                main_window.maximize()

            if event.key == pygame.K_n:
                main_window.minimize()

            if event.key == pygame.K_r:
                main_window.restore()

            if event.key == pygame.K_h:
                main_window.hide()
                pygame.time.set_timer(SHOW_WINDOW, 1000, 1)

            if event.key == pygame.K_s:
                win = pygame.Window("spawned window", (300, 300))
                try:
                    win.opacity = UNHOVERED_OPACITY
                except pygame.error:
                    pass
                windows_and_surfaces.append((win, win.get_surface()))

            if event.key == pygame.K_UP:
                for win, _ in windows_and_surfaces:
                    win.position += pygame.Vector2(0, -WIN_MOVE_SPEED)

            if event.key == pygame.K_DOWN:
                for win, _ in windows_and_surfaces:
                    win.position += pygame.Vector2(0, WIN_MOVE_SPEED)

            if event.key == pygame.K_LEFT:
                for win, _ in windows_and_surfaces:
                    win.position += pygame.Vector2(-WIN_MOVE_SPEED, 0)

            if event.key == pygame.K_RIGHT:
                for win, _ in windows_and_surfaces:
                    win.position += pygame.Vector2(WIN_MOVE_SPEED, 0)

            if event.key == pygame.K_1:
                for win, _ in windows_and_surfaces:
                    win.size -= pygame.Vector2(WIN_GROW_SPEED, WIN_GROW_SPEED)

            if event.key == pygame.K_2:
                for win, _ in windows_and_surfaces:
                    win.size += pygame.Vector2(WIN_GROW_SPEED, WIN_GROW_SPEED)

    for i, win_surface in enumerate(windows_and_surfaces):
        win, surface = win_surface

        surface.fill(COLOR_PROGRESSION[win.id % len(COLOR_PROGRESSION)])
        if surface == main_surface:
            centered_rect = rendered_instructions.get_rect(
                center=pygame.Vector2(win.size) / 2
            )
            surface.blit(rendered_instructions, centered_rect)
        win.flip()

    clock.tick(144)

pygame.quit()
