"""Pygame module to transform surfaces.

A Surface transform is an operation that moves or resizes the pixels. All these
functions take a Surface to operate on and return a new Surface with the
results.

Some of the transforms are considered destructive. These means every time they
are performed they lose pixel data. Common examples of this are resizing and
rotating. For this reason, it is better to re-transform the original surface
than to keep transforming an image multiple times. (For example, suppose you
are animating a bouncing spring which expands and contracts. If you applied the
size changes incrementally to the previous images, you would lose detail.
Instead, always begin with the original image and scale to the desired size.)

.. versionchangedold:: 2.0.2 transform functions now support keyword arguments.
"""

from typing import Literal, Optional, Union

from pygame.surface import Surface
from pygame.typing import ColorLike, Point, RectLike, SequenceLike

def flip(surface: Surface, flip_x: bool, flip_y: bool) -> Surface:
    """Flip vertically and horizontally.

    This can flip a Surface either vertically, horizontally, or both.
    The arguments ``flip_x`` and ``flip_y`` are booleans that control whether
    to flip each axis. Flipping a Surface is non-destructive and returns a new
    Surface with the same dimensions.
    """

def scale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
) -> Surface:
    """Resize to new resolution.

    Resizes the Surface to a new size, given as (width, height).
    This is a fast scale operation that does not sample the results.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must be the same as the size (width, height) passed
    in, and the same depth and format as the source Surface.

    .. versionchanged:: 2.2.1 internal scaling algorithm was replaced with a nearly
        equivalent one that is 40% faster. Scale results will be very slightly
        different.
    """

def scale_by(
    surface: Surface,
    factor: Union[float, SequenceLike[float]],
    dest_surface: Optional[Surface] = None,
) -> Surface:
    """Resize to new resolution, using scalar(s).

    Same as :func:`scale()`, but scales by some factor, rather than taking
    the new size explicitly. For example, :code:`transform.scale_by(surf, 3)`
    will triple the size of the surface in both dimensions. Optionally, the
    scale factor can be a sequence of two numbers, controlling x and y scaling
    separately. For example, :code:`transform.scale_by(surf, (2, 1))` doubles
    the image width but keeps the height the same.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must have the scaled dimensions
    (width * factor, height * factor) and same depth and format as the source Surface.

    .. versionadded:: 2.1.3
    """

def rotate(surface: Surface, angle: float) -> Surface:
    """Rotate an image.

    Unfiltered counterclockwise rotation. The angle argument represents degrees
    and can be any floating point value. Negative angle amounts will rotate
    clockwise.

    Unless rotating by 90 degree increments, the image will be padded larger to
    hold the new size. If the image has pixel alphas, the padded area will be
    transparent. Otherwise pygame will pick a color that matches the Surface
    colorkey or the topleft pixel value.
    """

def rotozoom(surface: Surface, angle: float, scale: float) -> Surface:
    """Filtered scale and rotation.

    This is a combined scale and rotation transform. The resulting Surface will
    be a filtered 32-bit Surface. The scale argument is a floating point value
    that will be multiplied by the current resolution. The angle argument is a
    floating point value that represents the counterclockwise degrees to rotate.
    A negative rotation angle will rotate clockwise.
    """

def scale2x(surface: Surface, dest_surface: Optional[Surface] = None) -> Surface:
    """Specialized image doubler.

    This will return a new image that is double the size of the original. It
    uses the AdvanceMAME Scale2X algorithm which does a 'jaggie-less' scale of
    bitmap graphics.

    This really only has an effect on simple images with solid colors. On
    photographic and antialiased images it will look like a regular unfiltered
    scale.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must have double the dimensions
    (width * 2, height * 2) and same depth and format as the source Surface.
    """

def smoothscale(
    surface: Surface,
    size: Point,
    dest_surface: Optional[Surface] = None,
) -> Surface:
    """Scale a surface to an arbitrary size smoothly.

    Uses one of two different algorithms for scaling each dimension of the input
    surface as required. For shrinkage, the output pixels are area averages of
    the colors they cover. The size is a 2 number sequence for (width, height).
    This function only works for 24-bit or 32-bit surfaces. A ``ValueError`` will
    be thrown if the input surface bit depth is less than 24.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must be the same as the size (width, height) passed
    in, and the same depth and format as the source Surface.

    .. versionaddedold:: 1.8

    .. versionchanged:: 2.4.0 now uses SSE2/NEON SIMD for acceleration on x86
        and ARM machines, a performance improvement over previous MMX/SSE only
        supported on x86.
    """

def smoothscale_by(
    surface: Surface,
    factor: Union[float, SequenceLike[float]],
    dest_surface: Optional[Surface] = None,
) -> Surface:
    """Resize to new resolution, using scalar(s).

    Same as :func:`smoothscale()`, but scales by some factor, rather than
    taking the new size explicitly. For example,
    :code:`transform.smoothscale_by(surf, 3)` will triple the size of the
    surface in both dimensions. Optionally, the scale factor can be a sequence
    of two numbers, controlling x and y scaling separately. For example,
    :code:`transform.smoothscale_by(surf, (2, 1))` doubles the image width but
    keeps the height the same.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must have the scaled dimensions
    (width * factor, height * factor) and same depth and format as the source Surface.

    .. versionadded:: 2.1.3
    """

def get_smoothscale_backend() -> Literal["GENERIC", "SSE2", "NEON"]:
    """Return smoothscale filter version in use: 'GENERIC', 'MMX', 'SSE', 'SSE2', or 'NEON'.

    Shows whether or not smoothscale is using SIMD acceleration.
    If no acceleration is available then "GENERIC" is returned. The level of
    acceleration possible is automatically determined at runtime.

    This function is provided for pygame testing and debugging.

    .. versionchanged:: 2.4.0 Added SSE2 and NEON backends, MMX and SSE are deprecated.
    """

def set_smoothscale_backend(backend: Literal["GENERIC", "SSE2", "NEON"]) -> None:
    """Set smoothscale filter version to one of: 'GENERIC', 'MMX', 'SSE', 'SSE2', or 'NEON'.

    Sets smoothscale acceleration. Takes a string argument. A value of 'GENERIC'
    turns off acceleration. A value error is raised if type is not
    recognized or not supported by the current processor.

    This function is provided for pygame testing and debugging. If smoothscale
    causes an invalid instruction error then it is a pygame/SDL bug that should
    be reported. Use this function as a temporary fix only.

    .. versionchanged:: 2.4.0 Added SSE2 and NEON backends, MMX and SSE are deprecated.
    """

def chop(surface: Surface, rect: RectLike) -> Surface:
    """Gets a copy of an image with an interior area removed.

    Extracts a portion of an image. All vertical and horizontal pixels
    surrounding the given rectangle area are removed. The corner areas (diagonal
    to the rect) are then brought together. (The original image is not altered
    by this operation.)

    ``NOTE``: If you want a "crop" that returns the part of an image within a
    rect, you can blit with a rect to a new surface or copy a subsurface.
    """

def laplacian(surface: Surface, dest_surface: Optional[Surface] = None) -> Surface:
    """Find edges in a surface.

    Finds the edges in a surface using the laplacian algorithm.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must have the same dimensions (width, height) and
    depth as the source Surface.

    .. versionaddedold:: 1.8
    """

def box_blur(
    surface: Surface,
    radius: int,
    repeat_edge_pixels: bool = True,
    dest_surface: Optional[Surface] = None,
) -> Surface:
    """Blur a surface using box blur.

    Returns the blurred surface using box blur algorithm.

    This function does not work for indexed surfaces.
    An exception will be thrown if the input is an indexed surface.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must have the same dimensions (width, height) and
    depth and format as the source Surface.

    .. versionadded:: 2.2.0

    .. versionchanged:: 2.3.0
        Passing the calling surface as destination surface raises a ``ValueError``

    .. versionchanged:: 2.5.0
        A surface with either width or height equal to 0 won't raise a ``ValueError``
    """

def gaussian_blur(
    surface: Surface,
    radius: int,
    repeat_edge_pixels: bool = True,
    dest_surface: Optional[Surface] = None,
) -> Surface:
    """Blur a surface using gaussian blur.

    Returns the blurred surface using gaussian blur algorithm.
    Slower than `box_blur()`.

    This function does not work for indexed surfaces.
    An exception will be thrown if the input is an indexed surface.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must have the same dimensions (width, height) and
    depth and format as the source Surface.

    .. versionadded:: 2.2.0

    .. versionchanged:: 2.3.0
        Passing the calling surface as destination surface raises a ``ValueError``

    .. versionchanged:: 2.3.1
        Now the standard deviation of the Gaussian kernel is equal to the radius.
        Blur results will be slightly different.

    .. versionchanged:: 2.5.0
        A surface with either width or height equal to 0 won't raise a ``ValueError``
    """

def average_surfaces(
    surfaces: SequenceLike[Surface],
    dest_surface: Optional[Surface] = None,
    palette_colors: Union[bool, int] = 1,
) -> Surface:
    """Find the average surface from many surfaces.

    Takes a sequence of surfaces and returns a surface with average colors from
    each of the surfaces.

    palette_colors - if true we average the colors in palette, otherwise we
    average the pixel values. This is useful if the surface is actually
    grayscale colors, and not palette colors.

    Note, this function currently does not handle palette using surfaces
    correctly.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must have the same dimensions (width, height) and
    depth as the first passed source Surface.

    .. versionaddedold:: 1.8
    .. versionaddedold:: 1.9 ``palette_colors`` argument
    """

def average_color(
    surface: Surface, rect: Optional[RectLike] = None, consider_alpha: bool = False
) -> tuple[int, int, int, int]:
    """Finds the average color of a surface.

    Finds the average color of a Surface or a region of a surface specified by a
    Rect, and returns it as a tuple of integers red, green, blue, and alpha.
    If consider_alpha is set to True, then alpha is taken into account
    (removing the black artifacts).

    .. versionaddedold:: 2.1.2 ``consider_alpha`` argument
    """

def invert(surface: Surface, dest_surface: Optional[Surface] = None) -> Surface:
    """Inverts the RGB elements of a surface.

    Inverts each RGB pixel contained within the Surface, does not affect alpha channel.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must have the same dimensions (width, height) and
    depth as the source Surface.

    .. versionadded:: 2.2.0
    """

def grayscale(surface: Surface, dest_surface: Optional[Surface] = None) -> Surface:
    """Grayscale a surface.

    Returns a grayscaled version of the original surface using the luminosity formula which weights red, green and blue according to their wavelengths.

    An optional destination surface can be passed which is faster than creating a new
    Surface. This destination surface must have the same dimensions (width, height) and
    depth as the source Surface.

    .. versionadded:: 2.1.4

    .. versionchanged:: 2.4.0 Adjusted formula slightly to support performance
        optimisation. It may return very slightly different pixels than before,
        but should run seven to eleven times faster on most systems.
    """

def solid_overlay(
    surface: Surface,
    color: ColorLike,
    dest_surface: Optional[Surface] = None,
    keep_alpha: bool = False,
) -> Surface:
    """Replaces non transparent pixels with the provided color.

    Returns a new version of the original surface with all non transparent pixels set to the color provided.

    An optional destination surface can be passed which is faster than creating a new
    Surface.
    This destination surface must have the same dimensions (width, height) and
    depth as the source Surface.

    :param pygame.Surface surface: The target surface.

    :param color: Color which all non transparent within the target surface must be set to.
    :type color: :data:`pygame.typing.ColorLike`

    :param dest_surface: Optional destination surface to which the changes will be applied.
    :type dest_surface: pygame.Surface or None

    :param bool keep_alpha: Optional parameter that controls whether to keep the surface alpha when replacing with the color.

    .. versionadded:: 2.5.2
    """

def threshold(
    dest_surface: Optional[Surface],
    surface: Surface,
    search_color: Optional[ColorLike],
    threshold: ColorLike = (0, 0, 0, 0),
    set_color: Optional[ColorLike] = (0, 0, 0, 0),
    set_behavior: int = 1,
    search_surf: Optional[Surface] = None,
    inverse_set: bool = False,
) -> int:
    """Finds which, and how many pixels in a surface are within a threshold of a 'search_color' or a 'search_surf'.

    This versatile function can be used for find colors in a 'surf' close to a 'search_color'
    or close to colors in a separate 'search_surf'.

    It can also be used to transfer pixels into a 'dest_surf' that match or don't match.

    By default it sets pixels in the 'dest_surf' where all of the pixels NOT within the
    threshold are changed to set_color. If inverse_set is optionally set to True,
    the pixels that ARE within the threshold are changed to set_color.

    If the optional 'search_surf' surface is given, it is used to threshold against
    rather than the specified 'set_color'. That is, it will find each pixel in the
    'surf' that is within the 'threshold' of the pixel at the same coordinates
    of the 'search_surf'.

    :param dest_surf: Surface we are changing. See 'set_behavior'.
        Should be None if counting (set_behavior is 0).
    :type dest_surf: pygame.Surface or None

    :param pygame.Surface surf: Surface we are looking at.

    :param search_color: Color we are searching for.
    :type color: :data:`pygame.typing.ColorLike`

    :param threshold: Within this distance from search_color (or search_surf).
        You can use a threshold of (r,g,b,a) where the r,g,b can have different
        thresholds. So you could use an r threshold of 40 and a blue threshold of 2
        if you like.
    :type color: :data:`pygame.typing.ColorLike`

    :param set_color: Color we set in dest_surf.
    :type color: :data:`pygame.typing.ColorLike` or ``None``

    :param int set_behavior:
        - set_behavior=1 (default). Pixels in dest_surface will be changed to 'set_color'.
        - set_behavior=0 we do not change 'dest_surf', just count. Make dest_surf=None.
        - set_behavior=2 pixels set in 'dest_surf' will be from 'surf'.

    :param search_surf:
        - search_surf=None (default). Search against 'search_color' instead.
        - search_surf=Surface. Look at the color in 'search_surf' rather than using 'search_color'.
    :type search_surf: pygame.Surface or None

    :param bool inverse_set:
        - False, default. Pixels outside of threshold are changed.
        - True, Pixels within threshold are changed.

    :rtype: int
    :returns: The number of pixels that are within the 'threshold' in 'surf'
        compared to either 'search_color' or `search_surf`.

    .. versionaddedold:: 1.8
    .. versionchangedold:: 1.9.4
        Fixed a lot of bugs and added keyword arguments. Test your code.
    """

def hsl(
    surface: Surface,
    hue: float = 0,
    saturation: float = 0,
    lightness: float = 0,
    dest_surface: Optional[Surface] = None,
) -> Surface:
    """Change the hue, saturation, and lightness of a surface.

    This function allows you to modify the hue, saturation, and lightness of a given surface.

    :param pygame.Surface surface: The surface to transform.

    :param float hue: The amount to change the hue. Positive values rotate the hue clockwise,
        while negative values rotate it counterclockwise. Value range: -360 to 360.

    :param float saturation: The amount to change the saturation. Positive values increase saturation,
        while negative values decrease it. Value range: -1 to 1.

    :param float lightness: The amount to change the lightness. Positive values increase lightness,
        while negative values decrease it. Value range: -1 to 1.

    :param pygame.Surface dest_surface: An optional destination surface to store the transformed image.
        If provided, it should have the same dimensions and depth as the source surface.

    :returns: A new surface with the hue, saturation, and lightness transformed.

    :Examples:

    Apply a hue rotation of 30 degrees, increase saturation by 20%, and decrease lightness by 10% to a surface:

    .. code-block:: python

        new_surf = hsl(original_surf, 30, 0.2, -0.1)

    .. versionadded:: 2.5.0
    """
