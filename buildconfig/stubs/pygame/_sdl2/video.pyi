from collections.abc import Generator, Iterable
from typing import Any, Optional, Union

from pygame.color import Color
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.window import Window as Window

from pygame.typing import ColorLike, RectLike, Point

WINDOWPOS_UNDEFINED: int
WINDOWPOS_CENTERED: int

MESSAGEBOX_ERROR: int
MESSAGEBOX_WARNING: int
MESSAGEBOX_INFORMATION: int

SCALEQUALITY_NEAREST: int
SCALEQUALITY_LINEAR: int
SCALEQUALITY_BEST: int

class RendererDriverInfo:
    name: str
    flags: int
    num_texture_formats: int
    max_texture_width: int
    max_texture_height: int

def get_drivers() -> Generator[RendererDriverInfo, None, None]: ...
def get_grabbed_window() -> Optional[Window]: ...
def messagebox(
    title: str,
    message: str,
    window: Optional[Window] = None,
    info: bool = False,
    warn: bool = False,
    error: bool = False,
    buttons: tuple[str, ...] = ("OK",),
    return_button: int = 0,
    escape_button: int = 0,
) -> int: ...

class Texture:
    def __init__(
        self,
        renderer: Renderer,
        size: Iterable[int],
        static: bool = False,
        streaming: bool = False,
        target: bool = False,
        scale_quality: Optional[int] = None,
    ) -> None: ...
    @staticmethod
    def from_surface(renderer: Renderer, surface: Surface) -> Texture: ...
    renderer: Renderer
    width: int
    height: int
    alpha: int
    blend_mode: int

    @property
    def color(self) -> Color: ...
    @color.setter
    def color(self, value: ColorLike) -> None: ...
    def get_rect(self, **kwargs: Any) -> Rect: ...
    def draw(
        self,
        srcrect: Optional[RectLike] = None,
        dstrect: Optional[RectLike] = None,
        angle: float = 0.0,
        origin: Optional[Iterable[int]] = None,
        flip_x: bool = False,
        flip_y: bool = False,
    ) -> None: ...
    def draw_triangle(
        self,
        p1_xy: Point,
        p2_xy: Point,
        p3_xy: Point,
        p1_uv: Point = (0.0, 0.0),
        p2_uv: Point = (1.0, 1.0),
        p3_uv: Point = (0.0, 1.0),
        p1_mod: Iterable[int] = (255, 255, 255, 255),
        p2_mod: Iterable[int] = (255, 255, 255, 255),
        p3_mod: Iterable[int] = (255, 255, 255, 255),
    ) -> None: ...
    def draw_quad(
        self,
        p1_xy: Point,
        p2_xy: Point,
        p3_xy: Point,
        p4_xy: Point,
        p1_uv: Point = (0.0, 0.0),
        p2_uv: Point = (1.0, 0.0),
        p3_uv: Point = (1.0, 1.0),
        p4_uv: Point = (0.0, 1.0),
        p1_mod: Iterable[int] = (255, 255, 255, 255),
        p2_mod: Iterable[int] = (255, 255, 255, 255),
        p3_mod: Iterable[int] = (255, 255, 255, 255),
        p4_mod: Iterable[int] = (255, 255, 255, 255),
    ) -> None: ...
    def update(self, surface: Surface, area: Optional[RectLike] = None) -> None: ...

class Image:
    def __init__(
        self,
        texture_or_image: Union[Texture, Image],
        srcrect: Optional[RectLike] = None,
    ) -> None: ...
    def get_rect(self) -> Rect: ...
    def draw(
        self, srcrect: Optional[RectLike] = None, dstrect: Optional[RectLike] = None
    ) -> None: ...
    angle: float
    origin: Optional[Iterable[float]]
    flip_x: bool
    flip_y: bool
    alpha: float
    blend_mode: int
    texture: Texture
    srcrect: Rect

    @property
    def color(self) -> Color: ...
    @color.setter
    def color(self, value: ColorLike) -> None: ...

class Renderer:
    def __init__(
        self,
        window: Window,
        index: int = -1,
        accelerated: int = -1,
        vsync: bool = False,
        target_texture: bool = False,
    ) -> None: ...
    @classmethod
    def from_window(cls, window: Window) -> Renderer: ...
    draw_blend_mode: int
    @property
    def draw_color(self) -> Color: ...
    @draw_color.setter
    def draw_color(self, value: ColorLike) -> None: ...
    def clear(self) -> None: ...
    def present(self) -> None: ...
    def get_viewport(self) -> Rect: ...
    def set_viewport(self, area: Optional[RectLike]) -> None: ...
    logical_size: Iterable[int]
    scale: Iterable[float]
    target: Optional[Texture]
    def blit(
        self,
        source: Union[Texture, Image],
        dest: Optional[RectLike] = None,
        area: Optional[RectLike] = None,
        special_flags: int = 0,
    ) -> Rect: ...
    def draw_line(self, p1: Point, p2: Point) -> None: ...
    def draw_point(self, point: Point) -> None: ...
    def draw_rect(self, rect: RectLike) -> None: ...
    def fill_rect(self, rect: RectLike) -> None: ...
    def draw_triangle(
        self, p1: Point, p2: Point, p3: Point
    ) -> None: ...
    def fill_triangle(
        self, p1: Point, p2: Point, p3: Point
    ) -> None: ...
    def draw_quad(
        self, p1: Point, p2: Point, p3: Point, p4: Point
    ) -> None: ...
    def fill_quad(
        self, p1: Point, p2: Point, p3: Point, p4: Point
    ) -> None: ...
    def to_surface(
        self, surface: Optional[Surface] = None, area: Optional[RectLike] = None
    ) -> Surface: ...
    @staticmethod
    def compose_custom_blend_mode(
        color_mode: tuple[int, int, int], alpha_mode: tuple[int, int, int]
    ) -> int: ...
