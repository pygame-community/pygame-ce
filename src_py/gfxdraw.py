import pygame
import math as _math
from pygame._gfxdraw import *  # pylint: disable=wildcard-import,unused-wildcard-import; lgtm[py/polluting-import]


_pi_quo_180 = 0.01745329251994329577


def pixel(surface, x, y, color, /):
    surface.set_at((x, y), color)


def hline(surface, x1, x2, y, color, /):
    pygame.draw.line(surface, color, (x1, y), (x2, y))


def vline(surface, x, y1, y2, color, /):
    pygame.draw.line(surface, color, (x, y1), (x, y2))


def line(surface, x1, y1, x2, y2, color, /):
    pygame.draw.line(surface, color, (x1, y1), (x2, y2))


def rectangle(surface, rect, color, /):
    pygame.draw.rect(surface, color, rect, 1)


def box(surface, rect, color, /):
    pygame.draw.rect(surface, color, rect)


def circle(surface, x, y, r, color, /):
    pygame.draw.circle(surface, color, (x, y), r, 1)


def aacircle(surface, x, y, r, color, /):
    pygame.draw.aacircle(surface, color, (x, y), r, 1)


def filled_circle(surface, x, y, r, color, /):
    pygame.draw.circle(surface, color, (x, y), r)


def ellipse(surface, x, y, rx, ry, color, /):
    pygame.draw.ellipse(surface, color, (x - rx, y - ry, rx * 2, ry * 2), 1)


# missing feature for aaellipse: pygame.draw.aaellipse


def filled_ellipse(surface, x, y, rx, ry, color, /):
    pygame.draw.ellipse(surface, color, (x - rx, y - ry, rx * 2, ry * 2))


def arc(surface, x, y, r, start_angle, atp_angle, color):
    pygame.draw.arc(
        surface,
        color,
        (x - r, y - r, r * 2, r * 2),
        -atp_angle * _pi_quo_180,
        -start_angle * _pi_quo_180,
        1,
    )


def pie(surface, x, y, r, start_angle, atp_angle, color):
    start = start_angle * _pi_quo_180
    end = atp_angle * _pi_quo_180
    pygame.draw.arc(
        surface,
        color,
        (x - r, y - r, r * 2, r * 2),
        -end,
        -start,
        1,
    )
    pygame.draw.line(
        surface, color, (x, y), (x + _math.cos(start) * r, y + _math.sin(start) * r)
    )
    pygame.draw.line(
        surface, color, (x, y), (x + _math.cos(end) * r, y + _math.sin(end) * r)
    )


def trigon(surface, x1, y1, x2, y2, x3, y3, color, /):
    pygame.draw.polygon(surface, color, ((x1, y1), (x2, y2), (x3, y3)), 1)


# replace with pygame.draw.aapolygon when possible
def aatrigon(surface, x1, y1, x2, y2, x3, y3, color, /):
    pygame.draw.aalines(surface, color, True, ((x1, y1), (x2, y2), (x3, y3)))


def filled_trigon(surface, x1, y1, x2, y2, x3, y3, color, /):
    pygame.draw.polygon(surface, color, ((x1, y1), (x2, y2), (x3, y3)))


def polygon(surface, points, color, /):
    pygame.draw.polygon(surface, color, points, 1)


# replace with pygame.draw.aapolygon when possible
def aapolygon(surface, points, color, /):
    pygame.draw.aalines(surface, color, True, points)


def filled_polygon(surface, points, color, /):
    pygame.draw.polygon(surface, color, points)


# don't know how to shim: textured_polygon

# missing feature for bezier: pygame.draw.bezier
