#!/usr/bin/env python
"""pygame.examples.eventlist

Learn about pygame events and input.

At the top of the screen are the state of several device values,
and a scrolling list of events are displayed on the bottom.

"""

usage = """
Mouse Controls
==============

- 1st button on mouse (left click) to toggle events 'grabbed'.
- 3rd button on mouse (right click) to toggle mouse visible.
- The window can be resized.
- Mouse the mouse around to see mouse events.
- If events grabbed and mouse invisible show virtual mouse coords.


Keyboard Joystick Controls
==========================

- press keys up an down to see events.
- you can see joystick events if any are plugged in.
"""

import pygame

try:
    import pygame._sdl2.controller

    pygame._sdl2.controller.init()
    SDL2 = True
except ImportError:
    SDL2 = False

img_on_off = []
font = None
last_key = None

# these are a running counter of mouse.get_rel() calls.
virtual_x = 0
virtual_y = 0


def showtext(win, pos, text, color, bgcolor):
    textimg = font.render(text, 1, color, bgcolor)
    win.blit(textimg, pos)
    return pos[0] + textimg.get_width() + 5, pos[1]


def drawstatus(win):
    global virtual_x, virtual_y
    bgcolor = 50, 50, 50
    win.fill(bgcolor, (0, 0, 640, 120))
    win.blit(font.render("Status Area", 1, (155, 155, 155), bgcolor), (2, 2))

    pos = showtext(win, (10, 30), "Mouse Focus", (255, 255, 255), bgcolor)
    win.blit(img_on_off[pygame.mouse.get_focused()], pos)

    pos = showtext(
        win, (pos[0] + 50, pos[1]), "Mouse visible", (255, 255, 255), bgcolor
    )
    win.blit(img_on_off[pygame.mouse.get_visible()], pos)

    pos = showtext(win, (330, 30), "Keyboard Focus", (255, 255, 255), bgcolor)
    win.blit(img_on_off[pygame.key.get_focused()], pos)

    pos = showtext(win, (10, 60), "Mouse Position(rel)", (255, 255, 255), bgcolor)
    rel = pygame.mouse.get_rel()
    virtual_x += rel[0]
    virtual_y += rel[1]

    mouse_data = tuple(list(pygame.mouse.get_pos()) + list(rel))
    p = "%s, %s (%s, %s)" % mouse_data
    showtext(win, pos, p, bgcolor, (255, 255, 55))

    pos = showtext(win, (330, 60), "Last Keypress", (255, 255, 255), bgcolor)
    if last_key:
        p = "%d, %s" % (last_key, pygame.key.name(last_key))
    else:
        p = "None"
    showtext(win, pos, p, bgcolor, (255, 255, 55))

    pos = showtext(win, (10, 90), "Input Grabbed", (255, 255, 255), bgcolor)
    win.blit(img_on_off[pygame.event.get_grab()], pos)

    is_virtual_mouse = pygame.event.get_grab() and not pygame.mouse.get_visible()
    pos = showtext(win, (330, 90), "Virtual Mouse", (255, 255, 255), bgcolor)
    win.blit(img_on_off[is_virtual_mouse], pos)
    if is_virtual_mouse:
        p = f"{virtual_x}, {virtual_y}"
        showtext(win, (pos[0] + 50, pos[1]), p, bgcolor, (255, 255, 55))


def drawhistory(win, history):
    img = font.render("Event History Area", 1, (155, 155, 155), (0, 0, 0))
    win.blit(img, (2, 132))

    img = font.render("\n".join(history), 1, (50, 200, 50), (0, 0, 0), wraplength=640)
    win.blit(img, (10, 250))


def draw_usage_in_history(history, text):
    for line in text.split("\n"):
        if "===" not in line and line != "":
            history.append(line)


def main():
    pygame.init()
    print(usage)

    win = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("Mouse Focus Workout. h key for help")

    global font
    font = pygame.Font(None, 26)

    global img_on_off
    img_on_off.append(font.render("Off", 1, (0, 0, 0), (255, 50, 50)))
    img_on_off.append(font.render("On", 1, (0, 0, 0), (50, 255, 50)))

    # stores lines of text representing what has gone through the event queue
    history = []

    # let's turn on the joysticks just so we can play with em
    for x in range(pygame.joystick.get_count()):
        if SDL2 and pygame._sdl2.controller.is_controller(x):
            c = pygame._sdl2.controller.Controller(x)
            txt = f"Enabled controller: {c.name}"
        else:
            j = pygame.joystick.Joystick(x)
            txt = f"Enabled joystick: {j.get_name()}"

        history.append(txt)

    if not pygame.joystick.get_count():
        history.append("No Joysticks to Initialize")

    going = True
    while going:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    going = False
                else:
                    global last_key
                    last_key = e.key
                if e.key == pygame.K_h:
                    draw_usage_in_history(history, usage)

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pygame.event.set_grab(not pygame.event.get_grab())

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                pygame.mouse.set_visible(not pygame.mouse.get_visible())

            if e.type != pygame.MOUSEMOTION:
                txt = f"{pygame.event.event_name(e.type)}: {e.dict}"
                history.append(txt)
                history = history[-13:]

            if e.type == pygame.VIDEORESIZE:
                win = pygame.display.set_mode(e.size, pygame.RESIZABLE)

            if e.type == pygame.QUIT:
                going = False

        drawstatus(win)
        drawhistory(win, history)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()
    raise SystemExit


if __name__ == "__main__":
    main()
