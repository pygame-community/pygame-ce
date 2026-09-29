from collections.abc import Iterable
from typing import Any, Protocol, final

from pygame.color import Color
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.typing import ColorLike, IntPoint, Point, RectLike, SequenceLike
from pygame.window import Window
from typing_extensions import Buffer  # collections.abc 3.12

class _DrawableClass(Protocol):
    # Object that has the draw method that accepts area and dest arguments
    def draw(self, area: RectLike | None = None, dest: RectLike | None = None): ...

@final
class GeometryMesh:
    """Pygame object storing vertices and indices of a 2D mesh for fast rendering

    Meant to be used with :meth:`Renderer.render_geometry`. Parses the input
    and stores it as C arrays to render a 2D mesh without wasting performance.
    The texture, if one is used, can be provided to the Renderer at the time of
    rendering. When updating the data, it is faster to call :meth:`GeometryMesh.update`
    if the length of data is the same.
    Vertices can represent any kind of 2D mesh. Usage of this object requires knowledge
    related to GPU rendering and is only meant as a fast wrapper of SDL functionality.

    :param vertices: A sequence of vertices. Each vertex should be a 3-element
                     sequence. The first item should be a Point-like representing the vertex
                     position in Renderer coordinates. The second item should be
                     a valid pygame color value. The third item should be a Point-like
                     representing the normalized texture coordinates the vertex will
                     use.
    :param indices: An optional sequence of integers representing indices of the vertices.
                    Commonly used to reduce the amount of vertices when they overlap. If
                    not specified, all vertices will be drawn in order. The indices must be
                    in bounds of the vertices and must be a valid amount to form complete
                    triplets of vertices, otherwise SDL will raise errors when rendering.

    .. note:: Creating an instance every frame defies the purpose of this object. Store it
              and update it only when necessary. If frequently changing transformations
              that offset/scale/rotate the whole mesh are required, consider the
              ``transform_matrix`` parameter of :meth:`Renderer.render_geometry`

    .. versionadded:: 2.5.8
    """

    def __init__(
        self,
        vertices: SequenceLike[tuple[Point, ColorLike, Point]],
        indices: SequenceLike[int] | None = None,
    ) -> None: ...
    def update(
        self,
        vertices: SequenceLike[tuple[Point, ColorLike, Point]],
        indices: SequenceLike[int] | None = None,
    ) -> None:
        """Update the stored vertices and indices with new data

        If the amount of vertices and indices are the same, the previous array is used,
        making it faster than re-instancing the object. Otherwise, behaves the same.

        Check the constructor paramters of :class:`GeometryMesh` to see what data
        to provide.
        """

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
        source: "Texture" | "Image" | _DrawableClass,
        dest: RectLike | None = None,
        area: RectLike | None = None,
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
    def set_viewport(self, area: RectLike | None) -> None: ...
    def render_geometry(
        self,
        mesh: GeometryMesh,
        texture: "Texture | None" = None,
        transform_matrix: SequenceLike[float] | Buffer | None = None,
    ) -> None:
        """Render a static 2D mesh

        This method provides a fully flexible wrapper around ``SDL_RenderGeometry``
        to allow the rendering of any 2D mesh, not limited to primitive shapes.
        Only use this functionality if you are familiar with GPU rendering, as it
        is not intuitive compared to standard pygame rendering.
        The transform matrix, if one is provided, will modify a cached copy of the
        vertices before they are rendered.

        :param mesh: The mesh to render. It must be a :class:`GeometryMesh` instance
                     to avoid re-parsing the input every frame, guaranteeing maximum
                     performance.
        :type mesh: :class:`GeometryMesh`
        :param texture: An optional :class:`Texture` instance that the mesh will be
                        rendered with. The texture coordinates of the vertices should
                        be normalized to represent portions of the texture.
        :type texture: :class:`Texture`| None
        :param transform_matrix: An optional matrix-like sequence/buffer representing
                                 the 2D affine transformation applied to each vertex.
                                 The expected layout for the matrix is:

                                  [ a, c, tx ]
                                  [ b, d, ty ]
                                  [ 0, 0, 1  ]

                                 Only the first two rows are required, other elements
                                 will be ignored. The provided object must either support
                                 the buffer protocol or be a 1D sequence (contiguous rows).

                                 While this transformation can include rotation and
                                 shearing, it is possible to construct a simple offset and
                                 scale transformation matrix:

                                  [scale_x, 0,       offset_x]
                                  [0,       scale_y, offset_y]
                                  [0,       0,       1       ]

                                 Where setting scale_x = scale_y = 1 and offset_x =
                                 offset_y = 0 produces no changes to the mesh. Consult
                                 online resources to combine more transformations.

        .. versionadded:: 2.5.8
        """

    def to_surface(
        self, surface: Surface | None = None, area: RectLike | None = None
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
    pass
