from pygame.surface import Surface

from pygame.typing import ColorLike, Point, RectLike, SequenceLike

def pixel(surface: Surface, x: int, y: int, color: ColorLike, /) -> None: ...
def hline(surface: Surface, x1: int, x2: int, y: int, color: ColorLike, /) -> None: ...
def vline(surface: Surface, x: int, y1: int, y2: int, color: ColorLike, /) -> None: ...
def line(
    surface: Surface, x1: int, y1: int, x2: int, y2: int, color: ColorLike, /
) -> None: ...
def rectangle(surface: Surface, rect: RectLike, color: ColorLike, /) -> None: ...
def box(surface: Surface, rect: RectLike, color: ColorLike, /) -> None: ...
def circle(surface: Surface, x: int, y: int, r: int, color: ColorLike, /) -> None: ...
def aacircle(surface: Surface, x: int, y: int, r: int, color: ColorLike, /) -> None: ...
def filled_circle(
    surface: Surface, x: int, y: int, r: int, color: ColorLike, /
) -> None: ...
def ellipse(
    surface: Surface, x: int, y: int, rx: int, ry: int, color: ColorLike, /
) -> None: ...
def aaellipse(
    surface: Surface, x: int, y: int, rx: int, ry: int, color: ColorLike, /
) -> None: ...
def filled_ellipse(
    surface: Surface, x: int, y: int, rx: int, ry: int, color: ColorLike, /
) -> None: ...
def arc(
    surface: Surface,
    x: int,
    y: int,
    r: int,
    start_angle: int,
    atp_angle: int,
    color: ColorLike, /
) -> None: ...
def pie(
    surface: Surface,
    x: int,
    y: int,
    r: int,
    start_angle: int,
    atp_angle: int,
    color: ColorLike, /
) -> None: ...
def trigon(
    surface: Surface,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    x3: int,
    y3: int,
    color: ColorLike, /
) -> None: ...
def aatrigon(
    surface: Surface,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    x3: int,
    y3: int,
    color: ColorLike, /
) -> None: ...
def filled_trigon(
    surface: Surface,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    x3: int,
    y3: int,
    color: ColorLike, /
) -> None: ...
def polygon(
    surface: Surface, points: SequenceLike[Point], color: ColorLike, /
) -> None: ...
def aapolygon(
    surface: Surface, points: SequenceLike[Point], color: ColorLike, /
) -> None: ...
def filled_polygon(
    surface: Surface, points: SequenceLike[Point], color: ColorLike, /
) -> None: ...
def textured_polygon(
    surface: Surface, points: SequenceLike[Point], texture: Surface, tx: int, ty: int, /
) -> None: ...
def bezier(
    surface: Surface, points: SequenceLike[Point], steps: int, color: ColorLike, /
) -> None: ...
