"""Pygame module for image masks.

Useful for fast pixel perfect collision detection. A mask uses 1 bit per-pixel
to store which parts collide.

.. versionaddedold:: 1.8

.. versionchangedold:: 2.0.2 Mask functions now support keyword arguments.

.. versionchangedold:: 2.0.2 Mask functions that take positions or offsets now
                    support :class:`pygame.math.Vector2` arguments.
"""

import sys
from typing import Any

from pygame.rect import Rect
from pygame.surface import Surface
from pygame.typing import ColorLike, Point, RectLike
from typing_extensions import deprecated  # added in 3.13

def from_surface(surface: Surface, threshold: int = 127) -> Mask:
    """Creates a Mask from the given surface.

    Creates a :class:`Mask` object from the given surface by setting all the
    opaque pixels and not setting the transparent pixels.

    If the surface uses a color-key, then it is used to decide which bits in
    the resulting mask are set. All the pixels that are **not** equal to the
    color-key are **set** and the pixels equal to the color-key are not set.

    If a color-key is not used, then the alpha value of each pixel is used to
    decide which bits in the resulting mask are set. All the pixels that have an
    alpha value **greater than** the ``threshold`` parameter are **set** and the
    pixels with an alpha value less than or equal to the ``threshold`` are
    not set.

    :param Surface surface: the surface to create the mask from
    :param int threshold: (optional) the alpha threshold (default is 127) to
        compare with each surface pixel's alpha value, if the ``surface`` is
        color-keyed this parameter is ignored

    :returns: a newly created :class:`Mask` object from the given surface
    :rtype: Mask

    .. note::
        This function is used to create the masks for
        :func:`pygame.sprite.collide_mask`.
    """

def from_threshold(
    surface: Surface,
    color: ColorLike,
    threshold: ColorLike = (0, 0, 0, 255),
    othersurface: Surface | None = None,
    palette_colors: int = 1,
) -> Mask:
    """Creates a mask by thresholding Surfaces.

    This is a more featureful method of getting a :class:`Mask` from a surface.

    If the optional ``othersurface`` is not used, all the pixels **within** the
    ``threshold`` of the ``color`` parameter are **set** in the resulting mask.

    If the optional ``othersurface`` is used, every pixel in the first surface
    that is **within** the ``threshold`` of the corresponding pixel in
    ``othersurface`` is **set** in the resulting mask.

    :param Surface surface: the surface to create the mask from
    :param color: color used to check if the surface's pixels are within the
        given ``threshold`` range, this parameter is ignored if the optional
        ``othersurface`` parameter is supplied
    :type color: :data:`pygame.typing.ColorLike`
    :param threshold: (optional) the threshold range used to check the difference
        between two colors (default is ``(0, 0, 0, 255)``)
    :type threshold: :data:`pygame.typing.ColorLike`
    :param Surface othersurface: (optional) used to check whether the pixels of
        the first surface are within the given ``threshold`` range of the pixels
        from this surface (default is ``None``)
    :param int palette_colors: (optional) indicates whether to use the palette
        colors or not, a nonzero value causes the palette colors to be used and a
        0 causes them not to be used (default is 1)

    :returns: a newly created :class:`Mask` object from the given surface
    :rtype: Mask
    """

class Mask:
    """Pygame object for representing 2D bitmasks.

    A ``Mask`` object is used to represent a 2D bitmask. Each bit in
    the mask represents a pixel. 1 is used to indicate a set bit and 0 is used
    to indicate an unset bit. Set bits in a mask can be used to detect collisions
    with other masks and their set bits.

    A filled mask has all of its bits set to 1, conversely an
    unfilled/cleared/empty mask has all of its bits set to 0. Masks can be
    created unfilled (default) or filled by using the ``fill`` parameter. Masks
    can also be cleared or filled using the :func:`pygame.mask.Mask.clear()` and
    :func:`pygame.mask.Mask.fill()` methods respectively.

    A mask's coordinates start in the top left corner at ``(0, 0)`` just like
    :mod:`pygame.Surface`. Individual bits can be accessed using the
    :func:`pygame.mask.Mask.get_at()` and :func:`pygame.mask.Mask.set_at()`
    methods.

    .. _mask-offset-label:

    The methods :meth:`overlap`, :meth:`overlap_area`, :meth:`overlap_mask`,
    :meth:`draw`, :meth:`erase`, and :meth:`convolve` use an offset parameter
    to indicate the offset of another mask's top left corner from the calling
    mask's top left corner. The calling mask's top left corner is considered to
    be the origin ``(0, 0)``. Offsets are a sequence of two values
    ``(x_offset, y_offset)``. Positive and negative offset values are supported.

    ::

                    0 to x (x_offset)
                    :    :
            0 ..... +----:---------+
            to      |    :         |
            y .......... +-----------+
         (y_offset) |    | othermask |
                    |    +-----------+
                    | calling_mask |
                    +--------------+

    :param size: the dimensions of the mask (width and height)
    :param bool fill: (optional) create an unfilled mask (default: ``False``) or
        filled mask (``True``)

    :returns: a newly created :class:`Mask` object
    :rtype: Mask

    .. versionchangedold:: 2.0.0
        Shallow copy support added. The :class:`Mask` class supports the special
        method ``__copy__()`` and shallow copying via ``copy.copy(mask)``.
    .. versionchangedold:: 2.0.0 Subclassing support added. The :class:`Mask` class
        can be used as a base class.
    .. versionchangedold:: 1.9.5 Added support for keyword arguments.
    .. versionchangedold:: 1.9.5 Added the optional keyword parameter ``fill``.
    .. versionchangedold:: 1.9.5 Added support for masks with a width and/or a
        height of 0.
    """

    def __init__(self, size: Point, fill: bool = False) -> None: ...
    def __copy__(self) -> Mask: ...
    def copy(self) -> Mask:
        """Returns a new copy of the mask.

        :returns: a new copy of this mask, the new mask will have the same width,
            height, and set/unset bits as the original
        :rtype: Mask

        .. note::
            If a mask subclass needs to copy any instance specific attributes
            then it should override the ``__copy__()`` method. The overridden
            ``__copy__()`` method needs to call ``super().__copy__()`` and then
            copy the required data as in the following example code.

            ::

                class SubMask(pygame.mask.Mask):
                    def __copy__(self):
                        new_mask = super().__copy__()
                        # Do any SubMask attribute copying here.
                        return new_mask

        .. versionaddedold:: 2.0.0
        """

    def get_size(self) -> tuple[int, int]:
        """Returns the size of the mask.

        :returns: the size of the mask, (width, height)
        :rtype: tuple(int, int)
        """

    def get_rect(self, **kwargs: Any) -> Rect:  # Dict type needs to be completed
        """Returns a Rect based on the size of the mask.

        Returns a new :class:`pygame.Rect` object based on the size of this mask.
        The rect's default position will be ``(0, 0)`` and its default width and
        height will be the same as this mask's. The rect's attributes can be
        altered via :class:`pygame.Rect` attribute keyword arguments/values passed
        into this method. As an example, ``a_mask.get_rect(center=(10, 5))`` would
        create a :class:`pygame.Rect` based on the mask's size centered at the
        given position.

        :param dict kwargs: :class:`pygame.Rect` attribute keyword arguments/values
            that will be applied to the rect

        :returns: A new :class:`pygame.Rect` object based on the size of this mask
            with any :class:`pygame.Rect` attribute keyword arguments/values applied
            to it
        :rtype: Rect

        .. versionaddedold:: 2.0.0
        """

    def get_at(self, pos: Point) -> int:
        """Gets the bit at the given position.

        :param pos: the position of the bit to get (x, y)

        :returns: 1 if the bit is set, 0 if the bit is not set
        :rtype: int

        :raises IndexError: if the position is outside of the mask's bounds
        """

    def set_at(self, pos: Point, value: int = 1) -> None:
        """Sets the bit at the given position.

        :param pos: the position of the bit to set (x, y)
        :param int value: any nonzero int will set the bit to 1, 0 will set the
            bit to 0 (default is 1)

        :returns: ``None``
        :rtype: NoneType

        :raises IndexError: if the position is outside of the mask's bounds
        """

    def overlap(self, other: Mask, offset: Point) -> tuple[int, int] | None:
        """Returns the point of intersection.

        Returns the first point of intersection encountered between this mask and
        ``other``. A point of intersection is 2 overlapping set bits.

        The current algorithm searches the overlapping area in
        ``sizeof(unsigned long int) * CHAR_BIT`` bit wide column blocks (the value
        of ``sizeof(unsigned long int) * CHAR_BIT`` is platform dependent, for
        clarity it will be referred to as ``W``). Starting at the top left corner
        it checks bits 0 to ``W - 1`` of the first row (``(0, 0)`` to
        ``(W - 1, 0)``) then continues to the next row (``(0, 1)`` to
        ``(W - 1, 1)``). Once this entire column block is checked, it continues to
        the next one (``W`` to ``2 * W - 1``). This is repeated until it finds a
        point of intersection or the entire overlapping area is checked.

        :param Mask other: the other mask to overlap with this mask
        :param offset: the offset of ``other`` from this mask, for more
            details refer to the :ref:`Mask offset notes <mask-offset-label>`

        :returns: point of intersection or ``None`` if no intersection
        :rtype: tuple(int, int) or NoneType
        """

    def overlap_area(self, other: Mask, offset: Point) -> int:
        """Returns the number of overlapping set bits.

        Returns the number of overlapping set bits between this mask and
        ``other``.

        This can be useful for collision detection. An approximate collision
        normal can be found by calculating the gradient of the overlapping area
        through the finite difference.

        ::

            dx = mask.overlap_area(other, (x + 1, y)) - mask.overlap_area(other, (x - 1, y))
            dy = mask.overlap_area(other, (x, y + 1)) - mask.overlap_area(other, (x, y - 1))

        :param Mask other: the other mask to overlap with this mask
        :param offset: the offset of ``other`` from this mask, for more
            details refer to the :ref:`Mask offset notes <mask-offset-label>`

        :returns: the number of overlapping set bits
        :rtype: int
        """

    def overlap_mask(self, other: Mask, offset: Point) -> Mask:
        """Returns a mask of the overlapping set bits.

        Returns a :class:`Mask`, the same size as this mask, containing the
        overlapping set bits between this mask and ``other``.

        :param Mask other: the other mask to overlap with this mask
        :param offset: the offset of ``other`` from this mask, for more
            details refer to the :ref:`Mask offset notes <mask-offset-label>`

        :returns: a newly created :class:`Mask` with the overlapping bits set
        :rtype: Mask
        """

    def fill(self) -> None:
        """Sets all bits to 1.

        Sets all bits in the mask to 1.

        :returns: ``None``
        :rtype: NoneType
        """

    def clear(self) -> None:
        """Sets all bits to 0.

        Sets all bits in the mask to 0.

        :returns: ``None``
        :rtype: NoneType
        """

    def invert(self) -> None:
        """Flips all the bits.

        Flips all of the bits in the mask. All the set bits are cleared to 0 and
        all the unset bits are set to 1.

        :returns: ``None``
        :rtype: NoneType
        """

    def scale(self, scale: Point) -> Mask:
        """Resizes a mask.

        Creates a new :class:`Mask` of the requested size with its bits scaled
        from this mask.

        :param scale: the width and height (size) of the mask to create

        :returns: a new :class:`Mask` object with its bits scaled from this mask
        :rtype: Mask

        :raises ValueError: if ``width < 0`` or ``height < 0``
        """

    def draw(self, other: Mask, offset: Point) -> None:
        """Draws a mask onto another.

        Performs a bitwise OR, drawing ``other`` onto this mask.

        :param Mask other: the mask to draw onto this mask
        :param offset: the offset of ``other`` from this mask, for more
            details refer to the :ref:`Mask offset notes <mask-offset-label>`

        :returns: ``None``
        :rtype: NoneType
        """

    def erase(self, other: Mask, offset: Point) -> None:
        """Erases a mask from another.

        Erases (clears) all bits set in ``other`` from this mask.

        :param Mask other: the mask to erase from this mask
        :param offset: the offset of ``other`` from this mask, for more
            details refer to the :ref:`Mask offset notes <mask-offset-label>`

        :returns: ``None``
        :rtype: NoneType
        """

    def count(self) -> int:
        """Returns the number of set bits.

        :returns: the number of set bits in the mask
        :rtype: int
        """

    def centroid(self) -> tuple[int, int]:
        """Returns the centroid of the set bits.

        Finds the centroid (the center mass of the set bits) for this mask.

        :returns: a coordinate tuple indicating the centroid of the mask, it will
            return ``(0, 0)`` if the mask has no bits set
        :rtype: tuple(int, int)
        """

    def angle(self) -> float:
        """Returns the orientation of the set bits.

        Finds the approximate orientation (from -90 to 90 degrees) of the set bits
        in the mask. This works best if performed on a mask with only one
        connected component.

        :returns: the orientation of the set bits in the mask, it will return
            ``0.0`` if the mask has no bits set
        :rtype: float

        .. note::
            See :meth:`connected_component` for details on how a connected
            component is calculated.
        """

    def outline(self, every: int = 1) -> list[tuple[int, int]]:
        """Returns a list of points outlining an object.

        Returns a list of points of the outline of the first connected component
        encountered in the mask. To find a connected component, the mask is
        searched per row (left to right) starting in the top left corner.

        The ``every`` optional parameter skips set bits in the outline. For
        example, setting it to 10 would return a list of every 10th set bit in the
        outline.

        :param int every: (optional) indicates the number of bits to skip over in
            the outline (default is 1)

        :returns: a list of points outlining the first connected component
            encountered, an empty list is returned if the mask has no bits set
        :rtype: list[tuple(int, int)]

        .. note::
            See :meth:`connected_component` for details on how a connected
            component is calculated.
        """

    def convolve(
        self,
        other: Mask,
        output: Mask | None = None,
        offset: Point = (0, 0),
    ) -> Mask:
        """Returns the convolution of this mask with another mask.

        Convolve this mask with the given ``other`` Mask.

        :param Mask other: mask to convolve this mask with
        :param output: (optional) mask for output (default is ``None``)
        :type output: Mask or NoneType
        :param offset: the offset of ``other`` from this mask, (default is
            ``(0, 0)``)

        :returns: a :class:`Mask` with the ``(i - offset[0], j - offset[1])`` bit
            set, if shifting ``other`` (such that its bottom right corner is at
            ``(i, j)``) causes it to overlap with this mask

            If an ``output`` Mask is specified, the output is drawn onto it and
            it is returned. Otherwise a mask of size ``(MAX(0, width + other mask's
            width - 1), MAX(0, height + other mask's height - 1))`` is created and
            returned.

        :rtype: Mask
        """

    def connected_component(self, pos: Point = ...) -> Mask:
        """Returns a mask containing a connected component.

        A connected component is a group (1 or more) of connected set bits
        (orthogonally and diagonally). The SAUF algorithm, which checks 8 point
        connectivity, is used to find a connected component in the mask.

        By default this method will return a :class:`Mask` containing the largest
        connected component in the mask. Optionally, a bit coordinate can be
        specified and the connected component containing it will be returned. If
        the bit at the given location is not set, the returned :class:`Mask` will
        be empty (no bits set).

        :param pos: (optional) selects the connected component that contains the
            bit at this position

        :returns: a :class:`Mask` object (same size as this mask) with the largest
            connected component from this mask, if this mask has no bits set then
            an empty mask will be returned

            If the ``pos`` parameter is provided then the mask returned will have
            the connected component that contains this position. An empty mask will
            be returned if the ``pos`` parameter selects an unset bit.
        :rtype: Mask

        :raises IndexError: if the optional ``pos`` parameter is outside of the
            mask's bounds
        """

    def connected_components(self, minimum: int = 0) -> list[Mask]:
        """Returns a list of masks of connected components.

        Provides a list containing a :class:`Mask` object for each connected
        component.

        :param int minimum: (optional) indicates the minimum number of bits (to
            filter out noise) per connected component (default is 0, which equates
            to no minimum and is equivalent to setting it to 1, as a connected
            component must have at least 1 bit set)

        :returns: a list containing a :class:`Mask` object for each connected
            component, an empty list is returned if the mask has no bits set
        :rtype: list[Mask]

        .. note::
            See :meth:`connected_component` for details on how a connected
            component is calculated.
        """

    def get_bounding_rects(self) -> list[Rect]:
        """Returns a list of bounding rects of connected components.

        Provides a list containing a bounding rect for each connected component.

        :returns: a list containing a bounding rect for each connected component,
            an empty list is returned if the mask has no bits set
        :rtype: list[Rect]

        .. note::
            See :meth:`connected_component` for details on how a connected
            component is calculated.
        """

    def to_surface(
        self,
        surface: Surface | None = None,
        setsurface: Surface | None = None,
        unsetsurface: Surface | None = None,
        setcolor: ColorLike | None = (255, 255, 255, 255),
        unsetcolor: ColorLike | None = (0, 0, 0, 255),
        dest: RectLike | Point = (0, 0),
        area: RectLike | None = None,
    ) -> Surface:
        """Returns a surface with the mask drawn on it`

        Draws this mask on the given surface. Set bits (bits set to 1) and unset
        bits (bits set to 0) can be drawn onto a surface.

        :param surface: (optional) Surface to draw mask onto, if no surface is
            provided one will be created (default is ``None``, which will cause a
            surface with the parameters
            ``Surface(size=mask.get_size(), flags=SRCALPHA, depth=32)`` to be
            created, drawn on, and returned)
        :type surface: Surface or None
        :param setsurface: (optional) use this surface's color values to draw
            set bits (default is ``None``), if this surface is smaller than the
            mask any bits outside its bounds will use the ``setcolor`` value
        :type setsurface: Surface or None
        :param unsetsurface: (optional) use this surface's color values to draw
            unset bits (default is ``None``), if this surface is smaller than the
            mask any bits outside its bounds will use the ``unsetcolor`` value
        :type unsetsurface: Surface or None
        :param setcolor: (optional) color to draw set bits (default is
            ``(255, 255, 255, 255)``, white), use ``None`` to skip drawing the set
            bits, the ``setsurface`` parameter (if set) will takes precedence over
            this parameter
        :type setcolor: :data:`pygame.typing.ColorLike` or ``None``
        :param unsetcolor: (optional) color to draw unset bits (default is
            ``(0, 0, 0, 255)``, black), use ``None`` to skip drawing the unset
            bits, the ``unsetsurface`` parameter (if set) will takes precedence
            over this parameter
        :type unsetcolor: :data:`pygame.typing.ColorLike` or ``None``
        :param dest: (optional) surface destination of where to position the
            topleft corner of the mask being drawn (default is ``(0, 0)``), if a
            Rect is used as the ``dest`` parameter, its ``x`` and ``y`` attributes
            will be used as the destination, **NOTE1:** rects with a negative width
            or height value will not be normalized before using their ``x`` and
            ``y`` values, **NOTE2:** this destination value is only used to
            position the mask on the surface, it does not offset the ``setsurface``
            and ``unsetsurface`` from the mask, they are always aligned with the
            mask (i.e. position ``(0, 0)`` on the mask always corresponds to
            position ``(0, 0)`` on the ``setsurface`` and ``unsetsurface``)
        :type dest: Rect or tuple(int, int) or list(int, int) or Vector2(int, int)
        :param area: (optional) rectangular portion of the mask to draw. It can be a
            rect-like object (a Rect, a tuple or a list with 4 numbers or an object with a
            rect attribute, etc) or it can be None (the default) in which case it will use the
            entire mask. If the given rect protrudes outside the bounds of the mask (as returned
            by :meth:`get_rect`), it will get clipped to fit those boundaries. If the final rect
            is smaller than the mask and no destination ``surface`` is given, the returned surface
            will have the same size as this final rect.
        :type area: Rect or rect-like object

        :returns: the ``surface`` parameter (or a newly created surface if no
            ``surface`` parameter was provided) with this mask drawn on it
        :rtype: Surface

        :raises ValueError: if the ``setsurface`` parameter or ``unsetsurface``
            parameter does not have the same format (bytesize/bitsize/alpha) as
            the ``surface`` parameter

        .. note ::
            To skip drawing the set bits, both ``setsurface`` and ``setcolor`` must
            be ``None``. The ``setsurface`` parameter defaults to ``None``, but
            ``setcolor`` defaults to a color value and therefore must be set to
            ``None``.

        .. note ::
            To skip drawing the unset bits, both ``unsetsurface`` and
            ``unsetcolor`` must be ``None``. The ``unsetsurface`` parameter
            defaults to ``None``, but ``unsetcolor`` defaults to a color value and
            therefore must be set to ``None``.

        .. versionaddedold:: 2.0.0

        .. versionchanged:: 2.5.6 Added the area keyword argument.
        """

    if sys.version_info >= (3, 12):
        def __buffer__(self, flags: int, /) -> memoryview[int]: ...
        def __release_buffer__(self, view: memoryview[int], /) -> None: ...

@deprecated("Use `Mask` instead (MaskType is an old alias)")
class MaskType(Mask): ...
