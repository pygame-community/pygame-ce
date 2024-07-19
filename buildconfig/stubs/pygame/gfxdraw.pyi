from pygame.surface import Surface
from typing_extensions import deprecated # added in 3.13

from ._common import ColorValue, Coordinate, RectValue, Sequence

@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.Surface.set_at` instead")
def pixel(surface: Surface, x: int, y: int, color: ColorValue, /) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.line` instead")
def hline(surface: Surface, x1: int, x2: int, y: int, color: ColorValue, /) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.line` instead")
def vline(surface: Surface, x: int, y1: int, y2: int, color: ColorValue, /) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.line` instead")
def line(
    surface: Surface, x1: int, y1: int, x2: int, y2: int, color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.rect` instead")
def rectangle(surface: Surface, rect: RectValue, color: ColorValue, /) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.rect` instead")
def box(surface: Surface, rect: RectValue, color: ColorValue, /) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.circle` instead")
def circle(surface: Surface, x: int, y: int, r: int, color: ColorValue, /) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.aacircle` instead")
def aacircle(surface: Surface, x: int, y: int, r: int, color: ColorValue, /) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.circle` instead")
def filled_circle(
    surface: Surface, x: int, y: int, r: int, color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.ellipse` instead")
def ellipse(
    surface: Surface, x: int, y: int, rx: int, ry: int, color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.aaellipse` instead") # not implemented yet
def aaellipse(
    surface: Surface, x: int, y: int, rx: int, ry: int, color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.ellipse` instead")
def filled_ellipse(
    surface: Surface, x: int, y: int, rx: int, ry: int, color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.arc` instead")
def arc(
    surface: Surface,
    x: int,
    y: int,
    r: int,
    start_angle: int,
    atp_angle: int,
    color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.arc` and `pygame.draw.line` instead")
def pie(
    surface: Surface,
    x: int,
    y: int,
    r: int,
    start_angle: int,
    atp_angle: int,
    color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.polygon` instead")
def trigon(
    surface: Surface,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    x3: int,
    y3: int,
    color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.aalines` instead") # should replace with aapolygon
def aatrigon(
    surface: Surface,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    x3: int,
    y3: int,
    color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.polygon` instead")
def filled_trigon(
    surface: Surface,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    x3: int,
    y3: int,
    color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.polygon` instead")
def polygon(
    surface: Surface, points: Sequence[Coordinate], color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.aalines` instead") # should replace with aapolygon
def aapolygon(
    surface: Surface, points: Sequence[Coordinate], color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.polygon` instead")
def filled_polygon(
    surface: Surface, points: Sequence[Coordinate], color: ColorValue, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION.")
def textured_polygon(
    surface: Surface, points: Sequence[Coordinate], texture: Surface, tx: int, ty: int, /
) -> None: ...
@deprecated("since GFX_DEPRECATED_VERSION. Use `pygame.draw.bezier` instead") # not implemented yet
def bezier(
    surface: Surface, points: Sequence[Coordinate], steps: int, color: ColorValue, /
) -> None: ...
