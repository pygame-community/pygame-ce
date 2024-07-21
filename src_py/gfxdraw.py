from typing_extensions import deprecated
import math as _math

import pygame
from pygame._gfxdraw import *  # pylint: disable=wildcard-import,unused-wildcard-import; lgtm[py/polluting-import]


_pi_quo_180 = 0.01745329251994329577


@deprecated(
    "The function `pixel` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.Surface.set_at` instead"
)
def pixel(surface, x, y, color, /):
    """pixel(surface, x, y, color, /) -> None
    draw a pixel
    """
    surface.set_at((x, y), color)


@deprecated(
    "The function `hline` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.line` instead"
)
def hline(surface, x1, x2, y, color, /):
    """hline(surface, x1, x2, y, color, /) -> None
    draw a horizontal line
    """
    pygame.draw.line(surface, color, (x1, y), (x2, y))


@deprecated(
    "The function `vline` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.line` instead"
)
def vline(surface, x, y1, y2, color, /):
    """vline(surface, x, y1, y2, color, /) -> None
    draw a vertical line
    """
    pygame.draw.line(surface, color, (x, y1), (x, y2))


@deprecated(
    "The function `line` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.line` instead"
)
def line(surface, x1, y1, x2, y2, color, /):
    """line(surface, x1, y1, x2, y2, color, /) -> None
    draw a line
    """
    pygame.draw.line(surface, color, (x1, y1), (x2, y2))


@deprecated(
    "The function `rectangle` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.rect` instead"
)
def rectangle(surface, rect, color, /):
    """rectangle(surface, rect, color, /) -> None
    draw a rectangle
    """
    pygame.draw.rect(surface, color, rect, 1)


@deprecated(
    "The function `box` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.rect` instead"
)
def box(surface, rect, color, /):
    """box(surface, rect, color, /) -> None
    draw a filled rectangle
    """
    pygame.draw.rect(surface, color, rect)


@deprecated(
    "The function `circle` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.circle` instead"
)
def circle(surface, x, y, r, color, /):
    """circle(surface, x, y, r, color, /) -> None
    draw a circle
    """
    pygame.draw.circle(surface, color, (x, y), r, 1)


@deprecated(
    "The function `aacircle` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.aacircle` instead"
)
def aacircle(surface, x, y, r, color, /):
    """aacircle(surface, x, y, r, color, /) -> None
    draw an antialiased circle
    """
    pygame.draw.aacircle(surface, color, (x, y), r, 1)


@deprecated(
    "The function `filled_circle` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.circle` instead"
)
def filled_circle(surface, x, y, r, color, /):
    """filled_circle(surface, x, y, r, color, /) -> None
    draw a filled circle
    """
    pygame.draw.circle(surface, color, (x, y), r)


@deprecated(
    "The function `ellipse` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.ellipse` instead"
)
def ellipse(surface, x, y, rx, ry, color, /):
    """ellipse(surface, x, y, rx, ry, color, /) -> None
    draw an ellipse
    """
    pygame.draw.ellipse(surface, color, (x - rx, y - ry, rx * 2, ry * 2), 1)


# missing feature for aaellipse: pygame.draw.aaellipse
# @deprecated("The function `aaellipse` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.aaellipse` instead") # not implemented yet
"""aaellipse(surface, x, y, rx, ry, color, /) -> None
draw an antialiased ellipse
"""


@deprecated(
    "The function `filled_ellipse` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.ellipse` instead"
)
def filled_ellipse(surface, x, y, rx, ry, color, /):
    """filled_ellipse(surface, x, y, rx, ry, color, /) -> None
    draw a filled ellipse
    """
    pygame.draw.ellipse(surface, color, (x - rx, y - ry, rx * 2, ry * 2))


@deprecated(
    "The function `arc` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.arc` instead"
)
def arc(surface, x, y, r, start_angle, stop_angle, color):
    """arc(surface, x, y, r, start_angle, stop_angle, color, /) -> None
    draw an arc
    """
    pygame.draw.arc(
        surface,
        color,
        (x - r, y - r, r * 2, r * 2),
        -stop_angle * _pi_quo_180,
        -start_angle * _pi_quo_180,
        1,
    )


@deprecated(
    "The function `pie` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.arc` and `pygame.draw.line` instead"
)
def pie(surface, x, y, r, start_angle, stop_angle, color):
    """pie(surface, x, y, r, start_angle, stop_angle, color, /) -> None
    draw a pie
    """
    start = start_angle * _pi_quo_180
    end = stop_angle * _pi_quo_180
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


@deprecated(
    "The function `trigon` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.polygon` instead"
)
def trigon(surface, x1, y1, x2, y2, x3, y3, color, /):
    """trigon(surface, x1, y1, x2, y2, x3, y3, color, /) -> None
    draw a trigon/triangle
    """
    pygame.draw.polygon(surface, color, ((x1, y1), (x2, y2), (x3, y3)), 1)


# replace with pygame.draw.aapolygon when possible
@deprecated(
    "The function `aatrigon` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.aalines` instead"
)  # should replace with aapolygon
def aatrigon(surface, x1, y1, x2, y2, x3, y3, color, /):
    """aatrigon(surface, x1, y1, x2, y2, x3, y3, color, /) -> None
    draw an antialiased trigon/triangle
    """
    pygame.draw.aalines(surface, color, True, ((x1, y1), (x2, y2), (x3, y3)))


@deprecated(
    "The function `filled_trigon` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.polygon` instead"
)
def filled_trigon(surface, x1, y1, x2, y2, x3, y3, color, /):
    """filled_trigon(surface, x1, y1, x2, y2, x3, y3, color, /) -> None
    draw a filled trigon/triangle
    """
    pygame.draw.polygon(surface, color, ((x1, y1), (x2, y2), (x3, y3)))


@deprecated(
    "The function `polygon` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.polygon` instead"
)
def polygon(surface, points, color, /):
    """polygon(surface, points, color, /) -> None
    draw a polygon
    """
    pygame.draw.polygon(surface, color, points, 1)


# replace with pygame.draw.aapolygon when possible
@deprecated(
    "The function `aapolygon` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.aalines` instead"
)  # should replace with aapolygon
def aapolygon(surface, points, color, /):
    """aapolygon(surface, points, color, /) -> None
    draw an antialiased polygon
    """
    pygame.draw.aalines(surface, color, True, points)


@deprecated(
    "The function `filled_polygon` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.polygon` instead"
)
def filled_polygon(surface, points, color, /):
    """filled_polygon(surface, points, color, /) -> None
    draw a filled polygon
    """
    pygame.draw.polygon(surface, color, points)


# don't know how to shim: textured_polygon
# @deprecated("The function `textured_polygon` is deprecated since GFX_DEPRECATED_VERSION.")
"""textured_polygon(surface, points, texture, tx, ty, /) -> None
draw a textured polygon
"""

# missing feature for bezier: pygame.draw.bezier
# @deprecated("The function `bezier` is deprecated since GFX_DEPRECATED_VERSION. Use `pygame.draw.bezier` instead") # not implemented yet
"""bezier(surface, points, steps, color, /) -> None
draw a Bezier curve
"""

del deprecated
