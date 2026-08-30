"""Experimental pygame module porting the SDL render video system

The SDL render video system supports both software and GPU-accelerated
rendering through the Renderer, Texture and Image objects.

.. versionadded:: 2.5.4
"""

# render.rst contents for the future
"""
.. include:: common.txt

:mod:`pygame._render`
=====================

.. warning::
   This module isn't ready for prime time yet, it's still in development.
   These docs are primarily meant to help the pygame developers and
   super-early adopters who are in communication with the developers.
   This API will change.

   Also, this module is a C implementation of most of the features of the
   sdl2_video module. It is currently incomplete.

.. autopgmodule:: pygame._render
   :members:

"""

from collections.abc import Iterable
from typing import Any, Protocol, final

from pygame.color import Color
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.typing import ColorLike, IntPoint, Point, RectLike, SequenceLike
from pygame.window import Window

class _DrawableClass(Protocol):
    # Object that has the draw method that accepts area and dest arguments
    def draw(self, area: RectLike | None = None, dest: RectLike | None = None): ...

@final
class Renderer:
    """Object wrapping a 2D rendering context for a window

    :class:`Renderer` objects provide a cross-platform API for rendering 2D
    graphics onto a :class:`Window`, by using either Metal (macOS), OpenGL
    (macOS, Windows, Linux) or Direct3D (Windows) rendering drivers, depending
    on what is set or is available on a system during their creation.

    They can be used to draw both :class:`Texture` objects and simple points,
    lines and rectangles (which are colored based on :attr:`Renderer.draw_color`).

    If configured correctly and supported by an underlying rendering driver, Renderer
    objects can have a :class:`Texture` object temporarily set as a target texture
    (the Texture object must have been created with target texture usage support),
    which allows those textures to be drawn onto.

    To present drawn content onto the window, :meth:`Renderer.present` should be
    called. :meth:`Renderer.clear` should be called to clear any drawn content
    with the set Renderer draw color.

    When things are drawn onto Renderer objects, an internal batching system is
    used by default to batch those "draw calls" together, to have all of them be
    processed in one go when :meth:`Renderer.present` is called. This is unlike
    :class:`pygame.Surface` objects, on which modifications via blitting occur
    immediately, but lends well to the behavior of GPUs, as draw calls can be
    expensive on lower-end models.

    .. versionadded:: 2.5.4
    """

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
        source: "Texture" | "Image" | _DrawableClass,
        dest: RectLike | None = None,
        area: RectLike | None = None,
        special_flags: int = 0,
    ) -> Rect:
        """Draw textures using a Surface-like API

        For compatibility purposes. Draws :class:`Texture` objects onto the
        Renderer using a method signature similar to :meth:`pygame.Surface.blit`.

        :param source: A :class:`Texture` or :class:`Image` to draw.
        :param dest: The drawing destination on the rendering target.
        :param area: The portion of the source texture or image to draw from.
        :param special_flags: have no effect at this moment.

        .. note:: Textures created by different Renderers cannot shared with each other!

        .. versionadded:: 2.5.4
        """

    def clear(self) -> None:
        """Clear the current rendering target with the drawing color"""

    def draw_line(self, p1: Point, p2: Point) -> None:
        """Draw a line

        :param p1: The line start point.
        :param p2: The line end point.

        .. versionadded:: 2.5.4
        """

    def draw_point(self, point: Point) -> None:
        """Draw a point

        :param point: The point's coordinates.

        .. versionadded:: 2.5.4
        """

    def draw_quad(self, p1: Point, p2: Point, p3: Point, p4: Point) -> None:
        """Draw a quad outline

        :param p1: The first quad point.
        :param p2: The second quad point.
        :param p2: The third quad point.
        :param p2: The fourth quad point.

        .. versionadded:: 2.5.4
        """

    def draw_rect(self, rect: RectLike) -> None:
        """Draw a rectangle outline

        :param rect: The :class:`pygame.Rect`-like rectangle to draw.

        .. versionadded:: 2.5.4
        """

    def draw_triangle(self, p1: Point, p2: Point, p3: Point) -> None:
        """Draw a triangle outline

        :param p1: The first triangle point.
        :param p2: The second triangle point.
        :param p2: The third triangle point.

        .. versionadded:: 2.5.4
        """

    def fill_quad(self, p1: Point, p2: Point, p3: Point, p4: Point) -> None:
        """Draw a filled quad

        :param p1: The first quad point.
        :param p2: The second quad point.
        :param p2: The third quad point.
        :param p2: The fourth quad point.

        .. versionadded:: 2.5.4
        """

    def fill_rect(self, rect: RectLike) -> None:
        """Draw a filled rectangle

        :param rect: The :class:`pygame.Rect`-like rectangle to draw.

        .. versionadded:: 2.5.4
        """

    def fill_triangle(self, p1: Point, p2: Point, p3: Point) -> None:
        """Draw a filled triangle

        :param p1: The first triangle point.
        :param p2: The second triangle point.
        :param p2: The third triangle point.

        .. versionadded:: 2.5.4
        """

    def get_viewport(self) -> Rect:
        """Get the drawing area on the rendering target

        .. versionadded:: 2.5.4
        """

    def present(self) -> None:
        """Update the screen with any rendering performed since the previous call

        Presents the composed backbuffer to the screen.
        Updates the screen with any rendering performed since the previous call.

        .. versionadded:: 2.5.4
        """

    def set_viewport(self, area: Optional[RectLike]) -> None:
        """Set the drawing area on the rendering target

        :param area: A :class:`pygame.Rect` or tuple representing the
                   drawing area on the target, or ``None`` to use the
                   entire area of the current rendering target.

        .. versionadded:: 2.5.4
        """

    def coordinates_to_window(self, point: Point) -> tuple[float, float]: ...
    def coordinates_from_window(self, point: Point) -> tuple[float, float]: ...
    def to_surface(
        self, surface: Optional[Surface] = None, area: Optional[RectLike] = None
    ) -> Surface:
        """Read pixels from current rendering target and create a Surface (slow operation, use sparingly)

        Read pixel data from the current rendering target and return a
        :class:`pygame.Surface` containing it.

        :param Surface surface: A :class:`pygame.Surface` object to read the pixel
                                data into. It must be large enough to fit the area, otherwise
                                ``ValueError`` is raised.
                                If set to ``None``, a new surface will be created.
        :param area: The area of the screen to read pixels from. The area is
                    clipped to fit inside the viewport.
                    If ``None``, the entire viewport is used.

        .. note::
            This is a very slow operation, due to the overhead of the VRAM to RAM
            data transfer and the cost of creating a potentially large
            :class:`pygame.Surface`. It should not be used frequently.

        .. versionadded:: 2.5.4
        """

    @property
    def draw_blend_mode(self) -> int:
        """Get or set the blend mode used for primitive drawing operations

        .. versionadded:: 2.5.4
        """
    @draw_blend_mode.setter
    def draw_blend_mode(self, value: int) -> None: ...
    @property
    def draw_color(self) -> Color:
        """Get or set the color used for primitive drawing operations

        .. versionadded:: 2.5.4
        """
    @draw_color.setter
    def draw_color(self, value: ColorLike) -> None: ...
    @property
    def logical_size(self) -> tuple[int, int]:
        """Get or set the logical Renderer size (a device independent resolution for rendering)"""
    @logical_size.setter
    def logical_size(self, value: IntPoint) -> None: ...
    @property
    def scale(self) -> tuple[float, float]:
        """Get the drawing scale for the current rendering target

        .. versionadded:: 2.5.4
        """
    @scale.setter
    def scale(self, value: Point) -> None: ...
    @property
    def target(self) -> "Texture":
        """Get or set the current rendering target

        Gets or sets the current rendering target.
        A value of ``None`` means that no custom rendering target was set and the
        Renderer's window will be used as the target.

        .. versionadded:: 2.5.4
        """
    @target.setter
    def target(self, value: "Texture") -> None: ...
    @classmethod
    def compose_custom_blend_mode(
        cls, color_mode: SequenceLike[int], alpha_mode: SequenceLike[int]
    ) -> int:
        """Compose a custom blend mode

        Compose a custom blend mode.
        See https://wiki.libsdl.org/SDL2/SDL_ComposeCustomBlendMode for more information.

        :param color_mode: A tuple ``(srcColorFactor, dstColorFactor, colorOperation)``
        :param alpha_mode: A tuple ``(srcAlphaFactor, dstAlphaFactor, alphaOperation)``

        :return: A blend mode to be used with :meth:`Renderer.set_draw_blend_mode` and :meth:`Texture.set_blend_mode`.

        .. versionadded:: 2.5.4
        """

    @classmethod
    def from_window(cls, window: Window) -> Renderer:
        """Create a Renderer from an existing window

        .. versionadded:: 2.5.4
        """

@final
class Texture:
    """Pygame object that represents a texture

    .. versionadded:: 2.5.4
    """
    def __init__(
        self,
        renderer: Renderer,
        size: Iterable[int],
        depth: int = 0,
        static: bool = False,
        streaming: bool = False,
        target: bool = False,
        scale_quality: int | None = None,
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
        srcrect: RectLike | None = None,
        dstrect: RectLike | None = None,
        angle: float = 0.0,
        origin: Iterable[int] | None = None,
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
    def update(self, surface: Surface, area: RectLike | None = None) -> None: ...

@final
class Image:
    """Pygame object that represents a portion of a texture

    .. versionadded:: 2.5.4
    """
