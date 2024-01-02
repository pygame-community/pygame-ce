from typing import Any, Generator, Iterable, Optional, Tuple, Union

from pygame.color import Color
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.window import Window as Window

from .._common import ColorValue, RectValue, Coordinate

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
    buttons: Tuple[str, ...] = ("OK",),
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
        scale_quality: Optional[int] =None
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
    def color(self, value: ColorValue) -> None: ...

    def get_rect(self, **kwargs: Any) -> Rect: ...
    def draw(
        self,
        srcrect: Optional[RectValue] = None,
        dstrect: Optional[RectValue] = None,
        angle: float = 0.0,
        origin: Optional[Iterable[int]] = None,
        flip_x: bool = False,
        flip_y: bool = False,
    ) -> None: ...
    def draw_triangle(
        self,
        p1_xy: Coordinate,
        p2_xy: Coordinate,
        p3_xy: Coordinate,
        p1_uv: Coordinate = (0.0, 0.0),
        p2_uv: Coordinate = (1.0, 1.0),
        p3_uv: Coordinate = (0.0, 1.0),
        p1_mod: Iterable[int] = (255, 255, 255, 255),
        p2_mod: Iterable[int] = (255, 255, 255, 255),
        p3_mod: Iterable[int] = (255, 255, 255, 255),
    ) -> None: ...
    def draw_quad(
        self,
        p1_xy: Coordinate,
        p2_xy: Coordinate,
        p3_xy: Coordinate,
        p4_xy: Coordinate,
        p1_uv: Coordinate = (0.0, 0.0),
        p2_uv: Coordinate = (1.0, 0.0),
        p3_uv: Coordinate = (1.0, 1.0),
        p4_uv: Coordinate = (0.0, 1.0),
        p1_mod: Iterable[int] = (255, 255, 255, 255),
        p2_mod: Iterable[int] = (255, 255, 255, 255),
        p3_mod: Iterable[int] = (255, 255, 255, 255),
        p4_mod: Iterable[int] = (255, 255, 255, 255),
    ) -> None: ...
    def update(self, surface: Surface, area: Optional[RectValue] = None) -> None: ...

class Image:
    def __init__(
        self,
        texture_or_image: Union[Texture, Image],
        srcrect: Optional[RectValue] = None,
    ) -> None: ...
    def get_rect(self) -> Rect: ...
    def draw(
        self, srcrect: Optional[RectValue] = None, dstrect: Optional[RectValue] = None
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
    def color(self, value: ColorValue) -> None: ...

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
    def draw_color(self, value: ColorValue) -> None: ...
    def clear(self) -> None: ...
    def present(self) -> None: ...
    def get_viewport(self) -> Rect: ...
    def set_viewport(self, area: Optional[RectValue]) -> None: ...
    logical_size: Iterable[int]
    scale: Iterable[float]
    target: Optional[Texture]
    def blit(
        self,
        source: Union[Texture, Image],
        dest: Optional[RectValue] = None,
        area: Optional[RectValue] = None,
        special_flags: int = 0,
    ) -> Rect: ...
    def draw_line(self, p1: Coordinate, p2: Coordinate) -> None: ...
    def draw_point(self, point: Coordinate) -> None: ...
    def draw_rect(self, rect: RectValue) -> None: ...
    def fill_rect(self, rect: RectValue) -> None: ...
    def draw_triangle(
        self, p1: Coordinate, p2: Coordinate, p3: Coordinate
    ) -> None: ...
    def fill_triangle(
        self, p1: Coordinate, p2: Coordinate, p3: Coordinate
    ) -> None: ...
    def draw_quad(
        self, p1: Coordinate, p2: Coordinate, p3: Coordinate, p4: Coordinate
    ) -> None: ...
    def fill_quad(
        self, p1: Coordinate, p2: Coordinate, p3: Coordinate, p4: Coordinate
    ) -> None: ...
    def to_surface(
        self, surface: Optional[Surface] = None, area: Optional[RectValue] = None
    ) -> Surface: ...
    @staticmethod
    def compose_custom_blend_mode(
        color_mode: Tuple[int, int, int], alpha_mode: Tuple[int, int, int]
    ) -> int: ...
