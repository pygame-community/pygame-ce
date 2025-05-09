"""Pygame module for drawing shapes.

Draw several simple shapes to a surface. These functions will work for
rendering to any format of surface.

Most of the functions take a width argument to represent the size of stroke
(thickness) around the edge of the shape. If a width of 0 is passed the shape
will be filled (solid).

All the drawing functions respect the clip area for the surface and will be
constrained to that area. The functions return a rectangle representing the
bounding area of changed pixels. This bounding rectangle is the 'minimum'
bounding box that encloses the affected area.

All the drawing functions accept a color argument that is compatible with
:data:`pygame.typing.ColorLike`.

A color's alpha value will be written directly into the surface (if the
surface contains pixel alphas), but the draw function will not draw
transparently.

These functions temporarily lock the surface they are operating on. Many
sequential drawing calls can be sped up by locking and unlocking the surface
object around the draw calls (see :func:`pygame.Surface.lock` and
:func:`pygame.Surface.unlock`).

.. note ::
    See the :mod:`pygame.gfxdraw` module for alternative draw methods.
"""

from typing import overload

from pygame.rect import Rect
from pygame.surface import Surface
from pygame.typing import ColorLike, Point, RectLike, SequenceLike

def rect(
    surface: Surface,
    color: ColorLike,
    rect: RectLike,
    width: int = 0,
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1,
) -> Rect:
    """Draw a rectangle.

    Draws a rectangle on the given surface.

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param Rect rect: rectangle to draw, position and dimensions
    :param int width: (optional) used for line thickness or to indicate that
        the rectangle is to be filled (not to be confused with the width value
        of the ``rect`` parameter)

            | if ``width == 0``, (default) fill the rectangle
            | if ``width > 0``, used for line thickness
            | if ``width < 0``, nothing will be drawn
            |

    :param int border_radius: (optional) used for drawing rectangle with rounded corners.
        The supported range is [0, min(height, width) / 2], with 0 representing a rectangle
        without rounded corners.
    :param int border_top_left_radius: (optional) used for setting the value of top left
        border. If you don't set this value, it will use the border_radius value.
    :param int border_top_right_radius: (optional) used for setting the value of top right
        border. If you don't set this value, it will use the border_radius value.
    :param int border_bottom_left_radius: (optional) used for setting the value of bottom left
        border. If you don't set this value, it will use the border_radius value.
    :param int border_bottom_right_radius: (optional) used for setting the value of bottom right
        border. If you don't set this value, it will use the border_radius value.

            | if ``border_radius < 1`` it will draw rectangle without rounded corners
            | if any of border radii has the value ``< 0`` it will use value of the border_radius
            | If sum of radii on the same side of the rectangle is greater than the rect size the radii
            | will get scaled

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the position of the given ``rect``
        parameter and its width and height will be 0
    :rtype: Rect

    .. note::
        The :func:`pygame.Surface.fill()` method works just as well for drawing
        filled rectangles and can be hardware accelerated on some platforms.

    .. versionchangedold:: 2.0.0 Added support for keyword arguments.
    .. versionchangedold:: 2.0.0.dev8 Added support for border radius.
    .. versionchangedold:: 2.1.1
        Drawing rects with width now draws the width correctly inside the
        rect's area, rather than using an internal call to draw.lines(),
        which had half the width spill outside the rect area.
    """

def polygon(
    surface: Surface,
    color: ColorLike,
    points: SequenceLike[Point],
    width: int = 0,
) -> Rect:
    """Draw a polygon.

    Draws a polygon on the given surface.

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param points: a sequence of 3 or more (x, y) coordinates that make up the
        vertices of the polygon, each point in the sequence must be a
        tuple/list/:class:`pygame.math.Vector2` of 2 ints/floats,
        e.g. ``[(x1, y1), (x2, y2), (x3, y3)]``
    :type points: tuple(point) or list(point)
    :param int width: (optional) used for line thickness or to indicate that
        the polygon is to be filled

            | if width == 0, (default) fill the polygon
            | if width > 0, used for line thickness
            | if width < 0, nothing will be drawn
            |

            .. note::
                When using ``width`` values ``> 1``, the edge lines will grow
                outside the original boundary of the polygon. For more details on
                how the thickness for edge lines grow, refer to the ``width`` notes
                of the :func:`pygame.draw.line` function.

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the position of the first point in the
        ``points`` parameter (float values will be truncated) and its width and
        height will be 0
    :rtype: Rect

    :raises ValueError: if ``len(points) < 3`` (must have at least 3 points)
    :raises TypeError: if ``points`` is not a sequence or ``points`` does not
        contain number pairs

    .. note::
        For an aapolygon, use :func:`aalines()` with ``closed=True``.

    .. versionchangedold:: 2.0.0 Added support for keyword arguments.
    """

def circle(
    surface: Surface,
    color: ColorLike,
    center: Point,
    radius: float,
    width: int = 0,
    draw_top_right: bool = False,
    draw_top_left: bool = False,
    draw_bottom_left: bool = False,
    draw_bottom_right: bool = False,
) -> Rect:
    """Draw a circle.

    Draws a circle on the given surface.

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param center: center point of the circle as a sequence of 2 ints/floats,
        e.g. ``(x, y)``
    :type center: tuple(int or float, int or float) or
        list(int or float, int or float) or Vector2(int or float, int or float)
    :param radius: radius of the circle, measured from the ``center`` parameter,
        nothing will be drawn if the ``radius`` is less than 1
    :type radius: int or float
    :param int width: (optional) used for line thickness or to indicate that
        the circle is to be filled

            | if ``width == 0``, (default) fill the circle
            | if ``width > 0``, used for line thickness
            | if ``width < 0``, nothing will be drawn
            |

            .. note::
                When using ``width`` values ``> 1``, the edge lines will only grow
                inward.
    :param bool draw_top_right: (optional) if this is set to True then the top right corner
        of the circle will be drawn
    :param bool draw_top_left: (optional) if this is set to True then the top left corner
        of the circle will be drawn
    :param bool draw_bottom_left: (optional) if this is set to True then the bottom left corner
        of the circle will be drawn
    :param bool draw_bottom_right: (optional) if this is set to True then the bottom right corner
        of the circle will be drawn

            | if any of the draw_circle_part is True then it will draw all circle parts that have the True
            | value, otherwise it will draw the entire circle.

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the ``center`` parameter value (float
        values will be truncated) and its width and height will be 0
    :rtype: Rect

    :raises TypeError: if ``center`` is not a sequence of two numbers
    :raises TypeError: if ``radius`` is not a number

    .. versionchangedold:: 2.0.0 Added support for keyword arguments.
        Nothing is drawn when the radius is 0 (a pixel at the ``center`` coordinates
        used to be drawn when the radius equaled 0).
        Floats, and Vector2 are accepted for the ``center`` param.
        The drawing algorithm was improved to look more like a circle.
    .. versionchangedold:: 2.0.0.dev8 Added support for drawing circle quadrants.
    """

@overload
def aacircle(
    surface: Surface,
    color: ColorLike,
    center: Point,
    radius: float,
    width: int = 0,
) -> Rect: ...
@overload
def aacircle(
    surface: Surface,
    color: ColorLike,
    center: Point,
    radius: float,
    width: int = 0,
    draw_top_right: bool = False,
    draw_top_left: bool = False,
    draw_bottom_left: bool = False,
    draw_bottom_right: bool = False,
) -> Rect: ...
def aacircle(*args, **kwargs):  # type: ignore
    """Draw an antialiased circle.

    Draws an antialiased circle on the given surface.
    Uses Xiaolin Wu Circle Algorithm.
    adapted from: https://cgg.mff.cuni.cz/~pepca/ref/WU.pdf

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param center: center point of the circle as a sequence of 2 ints/floats,
        e.g. ``(x, y)``
    :type center: tuple(int or float, int or float) or
        list(int or float, int or float) or Vector2(int or float, int or float)
    :param radius: radius of the circle, measured from the ``center`` parameter,
        nothing will be drawn if the ``radius`` is less than 1
    :type radius: int or float
    :param int width: (optional) used for line thickness or to indicate that
        the circle is to be filled

            | if ``width == 0``, (default) fill the circle
            | if ``width > 0``, used for line thickness
            | if ``width < 0``, nothing will be drawn
            |

            .. note::
                When using ``width`` values ``> 1``, the edge lines will only grow
                inward.
    :param bool draw_top_right: (optional) if this is set to True then the top right corner
        of the circle will be drawn
    :param bool draw_top_left: (optional) if this is set to True then the top left corner
        of the circle will be drawn
    :param bool draw_bottom_left: (optional) if this is set to True then the bottom left corner
        of the circle will be drawn
    :param bool draw_bottom_right: (optional) if this is set to True then the bottom right corner
        of the circle will be drawn

            | if any of the draw_circle_part is True then it will draw all circle parts that have the True
            | value, otherwise it will draw the entire circle.

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the ``center`` parameter value (float
        values will be truncated) and its width and height will be 0
    :rtype: Rect

    :raises TypeError: if ``center`` is not a sequence of two numbers
    :raises TypeError: if ``radius`` is not a number

    .. versionadded:: 2.5.0
    """

def ellipse(surface: Surface, color: ColorLike, rect: RectLike, width: int = 0) -> Rect:
    """Draw an ellipse.

    Draws an ellipse on the given surface.

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param Rect rect: rectangle to indicate the position and dimensions of the
        ellipse, the ellipse will be centered inside the rectangle and bounded
        by it
    :param int width: (optional) used for line thickness or to indicate that
        the ellipse is to be filled (not to be confused with the width value
        of the ``rect`` parameter)

            | if ``width == 0``, (default) fill the ellipse
            | if ``width > 0``, used for line thickness
            | if ``width < 0``, nothing will be drawn
            |

            .. note::
                When using ``width`` values ``> 1``, the edge lines will only grow
                inward from the original boundary of the ``rect`` parameter.

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the position of the given ``rect``
        parameter and its width and height will be 0
    :rtype: Rect

    .. versionchangedold:: 2.0.0 Added support for keyword arguments.
    """

def arc(
    surface: Surface,
    color: ColorLike,
    rect: RectLike,
    start_angle: float,
    stop_angle: float,
    width: int = 1,
) -> Rect:
    """Draw an elliptical arc.

    Draws an elliptical arc on the given surface.

    The two angle arguments are given in radians and indicate the start and stop
    positions of the arc. The arc is drawn in a counterclockwise direction from
    the ``start_angle`` to the ``stop_angle``.

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param Rect rect: rectangle to indicate the position and dimensions of the
        ellipse which the arc will be based on, the ellipse will be centered
        inside the rectangle
    :param float start_angle: start angle of the arc in radians
    :param float stop_angle: stop angle of the arc in
        radians

            | if ``start_angle < stop_angle``, the arc is drawn in a
                counterclockwise direction from the ``start_angle`` to the
                ``stop_angle``
            | if ``start_angle > stop_angle``, tau (tau == 2 * pi) will be added
                to the ``stop_angle``, if the resulting stop angle value is greater
                than the ``start_angle`` the above ``start_angle < stop_angle`` case
                applies, otherwise nothing will be drawn
            | if ``start_angle == stop_angle``, nothing will be drawn

    :param int width: (optional) used for line thickness (not to be confused
        with the width value of the ``rect`` parameter)

            | if ``width == 0``, nothing will be drawn
            | if ``width > 0``, (default is 1) used for line thickness
            | if ``width < 0``, same as ``width == 0``

            .. note::
                When using ``width`` values ``> 1``, the edge lines will only grow
                inward from the original boundary of the ``rect`` parameter.

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the position of the given ``rect``
        parameter and its width and height will be 0
    :rtype: Rect

    .. versionchangedold:: 2.0.0 Added support for keyword arguments.
    """

def line(
    surface: Surface,
    color: ColorLike,
    start_pos: Point,
    end_pos: Point,
    width: int = 1,
) -> Rect:
    """Draw a straight line.

    Draws a straight line on the given surface. There are no endcaps. For thick
    lines the ends are squared off.

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param start_pos: start position of the line, (x, y)
    :type start_pos: tuple(int or float, int or float) or
        list(int or float, int or float) or Vector2(int or float, int or float)
    :param end_pos: end position of the line, (x, y)
    :type end_pos: tuple(int or float, int or float) or
        list(int or float, int or float) or Vector2(int or float, int or float)
    :param int width: (optional) used for line thickness

        | if width >= 1, used for line thickness (default is 1)
        | if width < 1, nothing will be drawn

        .. note::
            When using ``width`` values ``> 1``, lines will grow as follows.

            For odd ``width`` values, the thickness of each line grows with the
            original line being in the center.

            For even ``width`` values, the thickness of each line grows with the
            original line being offset from the center (as there is no exact
            center line drawn). As a result, lines with a slope < 1
            (horizontal-ish) will have 1 more pixel of thickness below the
            original line (in the y direction). Lines with a slope >= 1
            (vertical-ish) will have 1 more pixel of thickness to the right of
            the original line (in the x direction).

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the ``start_pos`` parameter value (float
        values will be truncated) and its width and height will be 0
    :rtype: Rect

    :raises TypeError: if ``start_pos`` or ``end_pos`` is not a sequence of
        two numbers

    .. versionchangedold:: 2.0.0 Added support for keyword arguments.
    """

def lines(
    surface: Surface,
    color: ColorLike,
    closed: bool,
    points: SequenceLike[Point],
    width: int = 1,
) -> Rect:
    """Draw multiple contiguous straight line segments.

    Draws a sequence of contiguous straight lines on the given surface. There are
    no endcaps or miter joints. For thick lines the ends are squared off.
    Drawing thick lines with sharp corners can have undesired looking results.

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param bool closed: if ``True`` an additional line segment is drawn between
        the first and last points in the ``points`` sequence
    :param points: a sequence of 2 or more (x, y) coordinates, where each
        point in the sequence must be a
        tuple/list/:class:`pygame.math.Vector2` of 2 ints/floats and adjacent
        points will be connected by a line segment, e.g. for the
        points ``[(x1, y1), (x2, y2), (x3, y3)]`` a line segment will be drawn
        from ``(x1, y1)`` to ``(x2, y2)`` and from ``(x2, y2)`` to ``(x3, y3)``,
        additionally if the ``closed`` parameter is ``True`` another line segment
        will be drawn from ``(x3, y3)`` to ``(x1, y1)``
    :type points: tuple(point) or list(point)
    :param int width: (optional) used for line thickness

            | if width >= 1, used for line thickness (default is 1)
            | if width < 1, nothing will be drawn

            .. note::
                When using ``width`` values ``> 1`` refer to the ``width`` notes
                of :func:`line` for details on how thick lines grow.

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the position of the first point in the
        ``points`` parameter (float values will be truncated) and its width and
        height will be 0
    :rtype: Rect

    :raises ValueError: if ``len(points) < 2`` (must have at least 2 points)
    :raises TypeError: if ``points`` is not a sequence or ``points`` does not
        contain number pairs

    .. versionchangedold:: 2.0.0 Added support for keyword arguments.
    """

def aaline(
    surface: Surface,
    color: ColorLike,
    start_pos: Point,
    end_pos: Point,
    width: int = 1,
) -> Rect:
    """Draw a straight antialiased line.

    Draws a straight antialiased line on the given surface. There are no endcaps.
    For thick lines the ends are squared off.

    .. note::
        Regarding float values for coordinates, a point with coordinate
        consisting of two whole numbers is considered being right in the center
        of said pixel (and having a height and width of 1 pixel would therefore
        completely cover it), while a point with coordinate where one (or both)
        of the numbers have non-zero decimal parts would be partially covering
        two (or four if both numbers have decimal parts) adjacent pixels, *e.g.*
        the point ``(1.4, 2)`` covers 60% of the pixel ``(1, 2)`` and 40% of the
        pixel ``(2,2)``.

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param start_pos: start position of the line, (x, y)
    :type start_pos: tuple(int or float, int or float) or
        list(int or float, int or float) or Vector2(int or float, int or float)
    :param end_pos: end position of the line, (x, y)
    :type end_pos: tuple(int or float, int or float) or
        list(int or float, int or float) or Vector2(int or float, int or float)
    :param int width: (optional) used for line thickness

            | if width >= 1, used for line thickness (default is 1)
            | if width < 1, nothing will be drawn

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the ``start_pos`` parameter value (float
        values will be truncated) and its width and height will be 0
    :rtype: Rect

    :raises TypeError: if ``start_pos`` or ``end_pos`` is not a sequence of
        two numbers

    .. versionchangedold:: 2.0.0 Added support for keyword arguments.
    .. versionchanged:: 2.4.0 Removed deprecated 'blend' argument
    .. versionchanged:: 2.5.0 ``blend`` argument re-added for backcompat, but will
        always raise a deprecation exception when used
    .. versionchanged:: 2.5.3 Added line width
    """

def aalines(
    surface: Surface,
    color: ColorLike,
    closed: bool,
    points: SequenceLike[Point],
) -> Rect:
    """Draw multiple contiguous straight antialiased line segments.

    Draws a sequence of contiguous straight antialiased lines on the given
    surface.

    :param Surface surface: surface to draw on
    :param color: color to draw with, the alpha value is optional if using a
        tuple ``(RGB[A])``
    :type color: :data:`pygame.typing.ColorLike`
    :param bool closed: if ``True`` an additional line segment is drawn between
        the first and last points in the ``points`` sequence
    :param points: a sequence of 2 or more (x, y) coordinates, where each
        point in the sequence must be a
        tuple/list/:class:`pygame.math.Vector2` of 2 ints/floats and adjacent
        points will be connected by a line segment, e.g. for the
        points ``[(x1, y1), (x2, y2), (x3, y3)]`` a line segment will be drawn
        from ``(x1, y1)`` to ``(x2, y2)`` and from ``(x2, y2)`` to ``(x3, y3)``,
        additionally if the ``closed`` parameter is ``True`` another line segment
        will be drawn from ``(x3, y3)`` to ``(x1, y1)``
    :type points: tuple(point) or list(point)

    :returns: a rect bounding the changed pixels, if nothing is drawn the
        bounding rect's position will be the position of the first point in the
        ``points`` parameter (float values will be truncated) and its width and
        height will be 0
    :rtype: Rect

    :raises ValueError: if ``len(points) < 2`` (must have at least 2 points)
    :raises TypeError: if ``points`` is not a sequence or ``points`` does not
        contain number pairs

    .. versionchangedold:: 2.0.0 Added support for keyword arguments.
    .. versionchanged:: 2.4.0 Removed deprecated ``blend`` argument
    .. versionchanged:: 2.5.0 ``blend`` argument re-added for backcompat, but will
        always raise a deprecation exception when used
    """
