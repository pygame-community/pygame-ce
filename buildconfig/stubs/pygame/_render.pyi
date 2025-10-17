from collections.abc import Iterable
from typing import Any, Optional, Protocol, Union, final

from pygame.color import Color
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.typing import ColorLike, IntPoint, Point, RectLike, SequenceLike
from pygame.window import Window

class _DrawableClass(Protocol):
    # Object that has the draw method that accepts area and dest arguments
    def draw(
        self, area: Optional[RectLike] = None, dest: Optional[RectLike] = None
    ): ...

@final
class Renderer:
    def __init__(
        self,
        window: Window,
        index: int = -1,
        accelerated: int = -1,
        vsync: bool = False,
        target_texture: bool = False,
    ) -> None: ...
    def blit(
        self,
        source: Union["Texture", "Image", _DrawableClass],
        dest: Optional[RectLike] = None,
        area: Optional[RectLike] = None,
        special_flags: int = 0,
    ) -> Rect: ...
    def clear(self) -> None: ...
    def draw_line(self, p1: Point, p2: Point) -> None: ...
    def draw_point(self, point: Point) -> None: ...
    def draw_quad(self, p1: Point, p2: Point, p3: Point, p4: Point) -> None: ...
    def draw_rect(self, rect: RectLike) -> None: ...
    def draw_triangle(self, p1: Point, p2: Point, p3: Point) -> None: ...
    def fill_quad(self, p1: Point, p2: Point, p3: Point, p4: Point) -> None: ...
    def fill_rect(self, rect: RectLike) -> None: ...
    def fill_triangle(self, p1: Point, p2: Point, p3: Point) -> None: ...
    def get_viewport(self) -> Rect: ...
    def coordinates_to_window(self, point: Point) -> tuple[float, float]: ...
    def coordinates_from_window(self, point: Point) -> tuple[float, float]: ...
    def present(self) -> None: ...
    def set_viewport(self, area: Optional[RectLike]) -> None: ...
    def to_surface(
        self, surface: Optional[Surface] = None, area: Optional[RectLike] = None
    ) -> Surface: ...
    @property
    def draw_blend_mode(self) -> int: ...
    @draw_blend_mode.setter
    def draw_blend_mode(self, value: int) -> None: ...
    @property
    def draw_color(self) -> Color: ...
    @draw_color.setter
    def draw_color(self, value: ColorLike) -> None: ...
    @property
    def logical_size(self) -> tuple[int, int]: ...
    @logical_size.setter
    def logical_size(self, value: IntPoint) -> None: ...
    @property
    def scale(self) -> tuple[float, float]: ...
    @scale.setter
    def scale(self, value: Point) -> None: ...
    @property
    def target(self) -> "Texture": ...
    @target.setter
    def target(self, value: "Texture") -> None: ...
    @classmethod
    def compose_custom_blend_mode(
        cls, color_mode: SequenceLike[int], alpha_mode: SequenceLike[int]
    ) -> int: ...
    @classmethod
    def from_window(cls, window: Window) -> Renderer: ...

@final
class Texture:
    def __init__(
        self,
        renderer: Renderer,
        size: Iterable[int],
        depth: int = 0,
        static: bool = False,
        streaming: bool = False,
        target: bool = False,
        scale_quality: Optional[int] = None,
    ) -> None: ...
    @property
    def alpha(self) -> int: ...
    @alpha.setter
    def alpha(self, value: int) -> None: ...
    @property
    def blend_mode(self) -> int: ...
    @blend_mode.setter
    def blend_mode(self, value: int) -> None: ...
    @property
    def color(self) -> Color: ...
    @color.setter
    def color(self, value: ColorLike) -> None: ...
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...
    @property
    def renderer(self) -> Renderer: ...
    @classmethod
    def from_surface(cls, renderer: Renderer, surface: Surface) -> Texture: ...
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
        p1_mod: ColorLike = (255, 255, 255, 255),
        p2_mod: ColorLike = (255, 255, 255, 255),
        p3_mod: ColorLike = (255, 255, 255, 255),
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
        p1_mod: ColorLike = (255, 255, 255, 255),
        p2_mod: ColorLike = (255, 255, 255, 255),
        p3_mod: ColorLike = (255, 255, 255, 255),
        p4_mod: ColorLike = (255, 255, 255, 255),
    ) -> None: ...
    def get_rect(self, **kwargs: Any) -> Rect: ...
    def update(self, surface: Surface, area: Optional[RectLike] = None) -> None: ...

@final
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
