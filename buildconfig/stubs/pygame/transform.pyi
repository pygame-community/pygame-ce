from typing import Optional, Union, Literal

from pygame.surface import Surface

from pygame.typing import ColorLike, Point, RectLike, SequenceLike

def flip(surface: Surface, flip_x: bool, flip_y: bool) -> Surface: ...
def scale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
) -> Surface: ...
def scale_by(
    surface: Surface,
    factor: Union[float, SequenceLike[float]],
    dest_surface: Optional[Surface] = None,
) -> Surface: ...
def rotate(surface: Surface, angle: float) -> Surface: ...
def rotozoom(surface: Surface, angle: float, scale: float) -> Surface: ...
def scale2x(surface: Surface, dest_surface: Optional[Surface] = None) -> Surface: ...
def grayscale(surface: Surface, dest_surface: Optional[Surface] = None) -> Surface: ...
def solid_overlay(
    surface: Surface,
    color: ColorLike,
    dest_surface: Optional[Surface] = None,
    keep_alpha: bool = False,
) -> Surface: ...
def smoothscale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
) -> Surface: ...
def smoothscale_by(
    surface: Surface,
    factor: Union[float, SequenceLike[float]],
    dest_surface: Optional[Surface] = None,
) -> Surface: ...
def get_smoothscale_backend() -> Literal["GENERIC", "SSE2", "NEON"]: ...
def set_smoothscale_backend(backend: Literal["GENERIC", "SSE2", "NEON"]) -> None: ...
def chop(surface: Surface, rect: RectLike) -> Surface: ...
def laplacian(surface: Surface, dest_surface: Optional[Surface] = None) -> Surface: ...
def invert(surface: Surface, dest_surface: Optional[Surface] = None) -> Surface: ...
def average_surfaces(
    surfaces: SequenceLike[Surface],
    dest_surface: Optional[Surface] = None,
    palette_colors: Union[bool, int] = 1,
) -> Surface: ...
def average_color(
    surface: Surface, rect: Optional[RectLike] = None, consider_alpha: bool = False
) -> tuple[int, int, int, int]: ...
def threshold(
    dest_surface: Optional[Surface],
    surface: Surface,
    search_color: Optional[ColorLike],
    threshold: ColorLike = (0, 0, 0, 0),
    set_color: Optional[ColorLike] = (0, 0, 0, 0),
    set_behavior: int = 1,
    search_surf: Optional[Surface] = None,
    inverse_set: bool = False,
) -> int: ...
def box_blur(
    surface: Surface,
    radius: int,
    repeat_edge_pixels: bool = True,
    dest_surface: Optional[Surface] = None
) -> Surface: ...
def gaussian_blur(
    surface: Surface,
    radius: int,
    repeat_edge_pixels: bool = True,
    dest_surface: Optional[Surface] = None
) -> Surface: ...
def hsl(
    surface: Surface,
    hue: float = 0,
    saturation: float = 0,
    lightness: float = 0,
    dest_surface: Optional[Surface] = None,
) -> Surface: ...
