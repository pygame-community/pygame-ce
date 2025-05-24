from collections.abc import Iterable
from typing import Any, Literal, Optional, Union, overload

from pygame.bufferproxy import BufferProxy
from pygame.color import Color
from pygame.rect import FRect, Rect
from pygame.typing import (
    ColorLike,
    Point,
    RectLike,
    SequenceLike,
)
from typing_extensions import deprecated  # added in 3.13

_ViewKind = Literal[
    "0",
    "1",
    "2",
    "3",
    b"0",
    b"1",
    b"2",
    b"3",
    "r",
    "g",
    "b",
    "a",
    "R",
    "G",
    "B",
    "A",
    b"r",
    b"g",
    b"b",
    b"a",
    b"R",
    b"G",
    b"B",
    b"A",
]

class Surface:
    """Pygame object for representing images.

    A pygame Surface is used to represent any image. The Surface has a fixed
    resolution and pixel format. Surfaces with 8-bit pixels use a color palette
    to map to 24-bit color.

    Call :meth:`pygame.Surface()` to create a new image object. The Surface will
    be cleared to all black. The only required arguments are the sizes. With no
    additional arguments, the Surface will be created in a format that best
    matches the display Surface.

    The pixel format can be controlled by passing the bit depth or an existing
    Surface. The flags argument is a bitmask of additional features for the
    surface. You can pass any combination of these flags:

    ::

        HWSURFACE    (obsolete in pygame 2) creates the image in video memory
        SRCALPHA     the pixel format will include a per-pixel alpha

    Both flags are only a request, and may not be possible for all displays and
    formats.

    Advanced users can combine a set of bitmasks with a depth value. The masks
    are a set of 4 integers representing which bits in a pixel will represent
    each color. Normal Surfaces should not require the masks argument.

    Surfaces can have many extra attributes like alpha planes, colorkeys, source
    rectangle clipping. These functions mainly effect how the Surface is blitted
    to other Surfaces. The blit routines will attempt to use hardware
    acceleration when possible, otherwise they will use highly optimized
    software blitting methods.

    There are three types of transparency supported in pygame: colorkeys,
    surface alphas, and pixel alphas. Surface alphas can be mixed with
    colorkeys, but an image with per pixel alphas cannot use the other modes.
    Colorkey transparency makes a single color value transparent. Any pixels
    matching the colorkey will not be drawn. The surface alpha value is a single
    value that changes the transparency for the entire image. A surface alpha of
    255 is opaque, and a value of 0 is completely transparent.

    Per pixel alphas are different because they store a transparency value for
    every pixel. This allows for the most precise transparency effects, but it
    also the slowest. Per pixel alphas cannot be mixed with surface alpha and
    colorkeys.

    There is support for pixel access for the Surfaces. Pixel access on hardware
    surfaces is slow and not recommended. Pixels can be accessed using the
    :meth:`get_at()` and :meth:`set_at()` functions. These methods are fine for
    simple access, but will be considerably slow when doing of pixel work with
    them. If you plan on doing a lot of pixel level work, it is recommended to
    use a :class:`pygame.PixelArray`, which gives an array like view of the
    surface. For involved mathematical manipulations try the
    :mod:`pygame.surfarray` module (It's quite quick, but requires NumPy.)

    Any functions that directly access a surface's pixel data will need that
    surface to be lock()'ed. These functions can :meth:`lock()` and
    :meth:`unlock()` the surfaces themselves without assistance. But, if a
    function will be called many times, there will be a lot of overhead for
    multiple locking and unlocking of the surface. It is best to lock the
    surface manually before making the function call many times, and then
    unlocking when you are finished. All functions that need a locked surface
    will say so in their docs. Remember to leave the Surface locked only while
    necessary.

    Surface pixels are stored internally as a single number that has all the
    colors encoded into it. Use the :meth:`map_rgb()` and
    :meth:`unmap_rgb()` to convert between individual red, green, and blue
    values into a packed integer for that Surface.

    Surfaces can also reference sections of other Surfaces. These are created
    with the :meth:`subsurface()` method. Any change to either Surface will
    effect the other.

    Each Surface contains a clipping area. By default the clip area covers the
    entire Surface. If it is changed, all drawing operations will only effect
    the smaller area.
    """

    @overload
    def __init__(
        self,
        size: Point,
        flags: int = 0,
        depth: int = 0,
        masks: Optional[ColorLike] = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        size: Point,
        flags: int = 0,
        surface: Surface = ...,
    ) -> None: ...
    def __copy__(self) -> Surface: ...
    def __deepcopy__(self, memo) -> Surface: ...
    def blit(
        self,
        source: Surface,
        dest: Union[Point, RectLike] = (0, 0),
        area: Optional[RectLike] = None,
        special_flags: int = 0,
    ) -> Rect:
        """Draw another surface onto this one.

        Draws another Surface onto this Surface.

        **Parameters**
            - ``source``
                The ``Surface`` object to draw onto this ``Surface``.
                If it has transparency, transparent pixels will be ignored when blittting to an 8-bit ``Surface``.
            - ``dest`` *(optional)*
                The ``source`` draw position onto this ``Surface``, defaults to (0, 0).
                It can be a coordinate pair ``(x, y)`` or a ``Rect`` (using its top-left corner).
                If a ``Rect`` is passed, its size will not affect the blit.
            - ``area`` *(optional)*
                The rectangular portion of the ``source`` to draw.
                It can be a ``Rect`` object representing that section. If ``None`` or not provided,
                the entire source surface will be drawn.
                If the ``Rect`` has negative position, the final blit position will be
                ``dest`` - ``Rect.topleft``.
            - ``special_flags`` *(optional)*
                Controls how the colors of the ``source`` are combined with this Surface.
                If not provided it defaults to ``BLENDMODE_NONE`` (``0``).
                See :doc:`special_flags_list` for a list of possible values.
        **Return**
            A :doc:`rect` object representing the affected area of this ``Surface`` that was modified
            by the blit operation. This area includes only the pixels within this ``Surface`` or
            its clipping area (see :meth:`set_clip`).
            Generally you don't need to use this return value, as it was initially designed to
            pass it to :meth:`pygame.display.update` to optimize the updating of the display.
            Since modern computers are fast enough to update the entire display at high speeds,
            this return value is rarely used nowadays.
        **Example Use**
            .. code-block:: python

                    # create a surface of size 50x50 and fill it with red color
                    red_surf = pygame.Surface((50, 50))
                    red_surf.fill("red")

                    # draw the surface on another surface at position (0, 0)
                    another_surface.blit(red_surf, (0, 0))

        **Notes**
            - When self-blitting and there is a colorkey or alpha transparency set, resulting colors
              may appear slightly different compared to a non-self blit.

            - The blit is ignored if the ``source`` is positioned completely outside this ``Surface``'s
              clipping area. Otherwise only the overlapping area will be drawn.

        .. versionchanged:: 2.5.1 The dest argument is optional and defaults to (0, 0)
        """

    def blits(
        self,
        blit_sequence: Iterable[
            Union[
                tuple[Surface, Union[Point, RectLike]],
                tuple[Surface, Union[Point, RectLike], Union[RectLike, int]],
                tuple[Surface, Union[Point, RectLike], RectLike, int],
            ]
        ],
        doreturn: Union[int, bool] = 1,
    ) -> Union[list[Rect], None]:
        """Draw many surfaces onto this surface at their corresponding location.

        The ``blits`` method efficiently draws a sequence of surfaces onto this ``Surface``.

        **Parameters**

            ``blit_sequence``
                A sequence that contains each surface to be drawn along with its associated blit
                arguments. See the **Sequence Item Formats** section below for the possible formats.

            ``doreturn`` (optional)
                The ``doreturn`` parameter controls the return value. When set to ``True``, it returns
                a list of rectangles representing the changed areas. When set to ``False``, returns
                ``None``.

        **Return**

            A list of rectangles or ``None``.

        **Sequence Item Formats**

            ``(source, dest)``
                - ``source``: Surface object to be drawn.
                - ``dest``: Position where the source Surface should be blitted.

            ``(source, dest, area)``
                - ``area``: (optional) Specific area of the source Surface to be drawn.

            ``(source, dest, area, special_flags)``
                - ``special_flags``: (optional) Controls the blending mode for drawing colors.
                  See :doc:`special_flags_list` for a list of possible values.

        **Notes**

            - ``blits`` is an advanced method. It is recommended to read the documentation
              of :meth:`blit` first.

            - To draw a ``Surface`` with a special flag, you must specify an area as well, e.g.,
              ``(source, dest, None, special_flags)``.

            - Prefer using :meth:`blits` over :meth:`blit` when drawing multiple surfaces
              for better performance. Use :meth:`blit` if you need to draw a single surface.

            - For drawing a sequence of (source, dest) pairs with whole source Surface
              and a singular special_flag, use the :meth:`fblits()` method.

        .. versionaddedold:: 1.9.4
        """

    def fblits(
        self,
        blit_sequence: Iterable[tuple[Surface, Union[Point, RectLike]]],
        special_flags: int = 0,
        /,
    ) -> None:
        """Draw many surfaces onto this surface at their corresponding location and with the same special_flags.

        This method takes a sequence of tuples (source, dest) as input, where source is a Surface
        object and dest is its destination position on this Surface. It draws each source Surface
        fully (meaning that unlike `blit()` you cannot pass an "area" parameter to represent
        a smaller portion of the source Surface to draw) on this Surface with the same blending
        mode specified by special_flags.

        :param blit_sequence: a sequence of (source, dest)
        :param special_flags: the flag(s) representing the blend mode used for each surface.
                            See :doc:`special_flags_list` for a list of possible values.

        :returns: ``None``

        .. note:: This method only accepts a sequence of (source, dest) pairs and a single
            special_flags value that's applied to all surfaces drawn. This allows faster
            iteration over the sequence and better performance over `blits()`. Further
            optimizations are applied if blit_sequence is a list or a tuple (using one
            of them is recommended).

        .. versionadded:: 2.1.4
        """

    @overload
    def convert(self, surface: Surface, /) -> Surface: ...
    @overload
    def convert(self, depth: int, flags: int = 0, /) -> Surface: ...
    @overload
    def convert(self, masks: ColorLike, flags: int = 0, /) -> Surface: ...
    @overload
    def convert(self) -> Surface: ...
    def convert(self, *args):  # type: ignore
        """Change the pixel format of a surface.

        Creates a new copy of the Surface with the pixel format changed. The new
        pixel format can be determined from another existing Surface. Otherwise
        depth, flags, and masks arguments can be used, similar to the
        :meth:`pygame.Surface()` call.

        If no arguments are passed the new Surface will have the same pixel
        format as the display Surface. This is always the fastest format for
        blitting. It is a good idea to convert all Surfaces before they are
        blitted many times.

        The converted Surface will have no pixel alphas. They will be stripped if
        the original had them. See :meth:`convert_alpha()` for preserving or
        creating per-pixel alphas.

        The new copy will have the same class as the copied surface. This lets
        a Surface subclass inherit this method without the need to override,
        unless subclass specific instance attributes also need copying.

        .. versionchanged:: 2.5.0 converting to a known format will succeed without
            a window/display surface.
        """

    def convert_alpha(self) -> Surface:
        """Change the pixel format of a surface including per pixel alphas.

        Creates a new copy of the surface with the desired pixel format. The new
        surface will be in a format suited for quick blitting to the display surface
        with per pixel alpha.

        Unlike the :meth:`convert()` method, the pixel format for the new
        surface will not be exactly the same as the display surface, but it will
        be optimized for fast alpha blitting to it.

        As with :meth:`convert()` the returned surface has the same class as
        the converted surface.

        .. versionchanged:: 2.4.0 'Surface' argument deprecated.
        """

    def copy(self) -> Surface:
        """Create a new copy of a Surface.

        Makes a duplicate copy of a Surface. The new surface will have the same
        pixel formats, color palettes, transparency settings, and class as the
        original. If a Surface subclass also needs to copy any instance specific
        attributes then it should override ``copy()``. Shallow copy and deepcopy
        are supported, Surface implements __copy__ and __deepcopy__ respectively.

        .. versionadded:: 2.3.1
            Added support for deepcopy by implementing __deepcopy__, calls copy() internally.
        """

    def fill(
        self,
        color: ColorLike,
        rect: Optional[RectLike] = None,
        special_flags: int = 0,
    ) -> Rect:
        """Fill Surface with a solid color.

        Fill the Surface with a solid color. If no rect argument is given the
        entire Surface will be filled. The rect argument will limit the fill to a
        specific area. The fill will also be contained by the Surface clip area.

        The color argument should be compatible with :data:`pygame.typing.ColorLike`.
        If using ``RGBA``, the Alpha (A part of ``RGBA``) is ignored unless the surface
        uses per pixel alpha (Surface has the ``SRCALPHA`` flag).

        The special_flags argument controls how the colors are combined. See :doc:`special_flags_list`
        for a list of possible values.

        This will return the affected Surface area.

        .. note:: As of pygame-ce version 2.5.1, a long-standing bug has been fixed!
            Now when passing in a ``Rect`` with negative ``x`` or negative ``y`` (or both),
            the ``Rect`` filled will no longer be shifted to ``(0, 0)``, but instead only the
            part of the ``Rect`` overlapping the window's ``Rect`` will be filled.
        """

    def scroll(self, dx: int = 0, dy: int = 0, scroll_flag: int = 0, /) -> None:
        """Shift the Surface pixels in place.

        Move the Surface by dx pixels right and dy pixels down. dx and dy may be
        negative for left and up scrolls respectively.

        Scrolling is contained by the Surface clip area. It is safe to have dx
        and dy values that exceed the surface size.

        The scroll flag can be:
            * ``0`` (default): the pixels are shifted but previous pixels are
              not modified.

            * ``pygame.SCROLL_ERASE``: the space created by the shifting pixels
              is filled with black or transparency.

            * ``pygame.SCROLL_REPEAT``: the pixels that disappear out of the
              surface or clip bounds are brought back on the opposite side
              resulting in an infinitely scrolling and repeating surface.

        .. versionaddedold:: 1.9

        .. versionchanged:: 2.5.3 Add repeating scroll and allow erasing pixels
        """

    @overload
    def set_colorkey(self, color: ColorLike, flags: int = 0, /) -> None: ...
    @overload
    def set_colorkey(self, color: None, /) -> None: ...
    def set_colorkey(self, *args):  # type: ignore
        """Set the transparent colorkey.

        Set the current color key for the Surface. When blitting this Surface
        onto a destination, any pixels that have the same color as the colorkey
        will be transparent. The color should be compatible with :data:`pygame.typing.ColorLike`.
        If ``None`` is passed, the colorkey will be unset.

        The colorkey will be ignored if the Surface is formatted to use per pixel
        alpha values. The colorkey can be mixed with the full Surface alpha
        value.

        The optional flags argument can be set to ``pygame.RLEACCEL`` to provide
        better performance on non accelerated displays. An ``RLEACCEL`` Surface
        will be slower to modify, but quicker to blit as a source.
        """

    def get_colorkey(self) -> Optional[tuple[int, int, int, int]]:
        """Get the current transparent colorkey.

        Return the current colorkey value for the Surface. If the colorkey is not
        set then ``None`` is returned.
        """

    @overload
    def set_alpha(self, value: int, flags: int = 0, /) -> None: ...
    @overload
    def set_alpha(self, value: None, /) -> None: ...
    def set_alpha(self, *args):  # type: ignore
        """Set the alpha value for the full Surface.

        Set the current alpha value for the Surface. When blitting this Surface
        onto a destination, the pixels will be drawn slightly transparent. The
        alpha value is an integer from 0 to 255, 0 is fully transparent and 255
        is fully opaque. If ``None`` is passed for the alpha value, then alpha
        blending will be disabled, including per-pixel alpha.

        This value is different than the per pixel Surface alpha. For a surface
        with per pixel alpha, blanket alpha is ignored and ``None`` is returned.

        .. versionchangedold:: 2.0 per-surface alpha can be combined with per-pixel
            alpha.

        The optional flags argument can be set to ``pygame.RLEACCEL`` to provide
        better performance on non accelerated displays. An ``RLEACCEL`` Surface
        will be slower to modify, but quicker to blit as a source.
        """

    def get_alpha(self) -> Optional[int]:
        """Get the current Surface transparency value.

        Return the current alpha value for the Surface.
        """

    def lock(self) -> None:
        """Lock the Surface memory for pixel access.

        Lock the pixel data of a Surface for access. On accelerated Surfaces, the
        pixel data may be stored in volatile video memory or nonlinear compressed
        forms. When a Surface is locked the pixel memory becomes available to
        access by regular software. Code that reads or writes pixel values will
        need the Surface to be locked.

        Surfaces should not remain locked for more than necessary. A locked
        Surface can often not be displayed or managed by pygame.

        Not all Surfaces require locking. The :meth:`mustlock()` method can
        determine if it is actually required. There is no performance penalty for
        locking and unlocking a Surface that does not need it.

        All pygame functions will automatically lock and unlock the Surface data
        as needed. If a section of code is going to make calls that will
        repeatedly lock and unlock the Surface many times, it can be helpful to
        wrap the block inside a lock and unlock pair.

        It is safe to nest locking and unlocking calls. The surface will only be
        unlocked after the final lock is released.
        """

    def unlock(self) -> None:
        """Unlock the Surface memory from pixel access.

        Unlock the Surface pixel data after it has been locked. The unlocked
        Surface can once again be drawn and managed by pygame. See the
        :meth:`lock()` documentation for more details.

        All pygame functions will automatically lock and unlock the Surface data
        as needed. If a section of code is going to make calls that will
        repeatedly lock and unlock the Surface many times, it can be helpful to
        wrap the block inside a lock and unlock pair.

        It is safe to nest locking and unlocking calls. The surface will only be
        unlocked after the final lock is released.
        """

    def mustlock(self) -> bool:
        """Test if the Surface requires locking.

        Returns ``True`` if the Surface is required to be locked to access pixel
        data. Usually pure software Surfaces do not require locking. This method
        is rarely needed, since it is safe and quickest to just lock all Surfaces
        as needed.

        All pygame functions will automatically lock and unlock the Surface data
        as needed. If a section of code is going to make calls that will
        repeatedly lock and unlock the Surface many times, it can be helpful to
        wrap the block inside a lock and unlock pair.
        """

    def get_locked(self) -> bool:
        """Test if the Surface is current locked.

        Returns ``True`` when the Surface is locked. It doesn't matter how many
        times the Surface is locked.
        """

    def get_locks(self) -> tuple[Any, ...]:
        """Gets the locks for the Surface.

        Returns the currently existing locks for the Surface.
        """

    def get_at(self, x_y: Point, /) -> Color:
        """Get the color value at a single pixel.

        Return a copy of the ``RGBA`` Color value at the given pixel. If the
        Surface has no per pixel alpha, then the alpha value will always be 255
        (opaque). If the pixel position is outside the area of the Surface an
        ``IndexError`` exception will be raised.

        Getting and setting pixels one at a time is generally too slow to be used
        in a game or realtime situation. It is better to use methods which
        operate on many pixels at a time like with the blit, fill and draw
        methods - or by using :mod:`pygame.surfarray`/:mod:`pygame.PixelArray`.

        This function will temporarily lock and unlock the Surface as needed.

        .. versionchanged:: 2.3.1 can now also accept both float coordinates and
            Vector2s for pixels.

        .. versionchangedold:: 1.9
            Returning a Color instead of tuple. Use ``tuple(surf.get_at((x,y)))``
            if you want a tuple, and not a Color. This should only matter if
            you want to use the color as a key in a dict.
        """

    def set_at(self, x_y: Point, color: ColorLike, /) -> None:
        """Set the color value for a single pixel.

        Set the color of a single pixel at the specified coordinates to be a
        :data:`pygame.typing.ColorLike` value. If the Surface does not have per pixel alphas,
        the alpha value is ignored. Setting pixels outside the Surface area or outside
        the Surface clipping will have no effect.

        Getting and setting pixels one at a time is generally too slow to be used
        in a game or realtime situation.

        This function will temporarily lock and unlock the Surface as needed.

        .. note:: If the surface is palettized, the pixel color will be set to the
            most similar color in the palette.

        .. versionchanged:: 2.3.1 can now also accept both float coordinates and
            Vector2s for pixels.
        """

    def get_at_mapped(self, x_y: Point, /) -> int:
        """Get the mapped color value at a single pixel.

        Return the integer value of the given pixel. If the pixel position is
        outside the area of the Surface an ``IndexError`` exception will be
        raised.

        This method is intended for pygame unit testing. It unlikely has any use
        in an application.

        This function will temporarily lock and unlock the Surface as needed.

        .. versionaddedold:: 1.9.2

        .. versionchanged:: 2.3.1 can now also accept both float coordinates and
            Vector2s for pixels.
        """

    def get_palette(self) -> list[Color]:
        """Get the color index palette for an 8-bit Surface.

        Return a list of up to 256 color elements that represent the indexed
        colors used in an 8-bit Surface. The returned list is a copy of the
        palette, and changes will have no effect on the Surface.

        Returning a list of ``Color(with length 3)`` instances instead of tuples.

        .. versionaddedold:: 1.9
        """

    def get_palette_at(self, index: int, /) -> Color:
        """Get the color for a single entry in a palette.

        Returns the red, green, and blue color values for a single index in a
        Surface palette. The index should be a value from 0 to 255.

        .. versionaddedold:: 1.9
            Returning ``Color(with length 3)`` instance instead of a tuple.
        """

    def set_palette(self, palette: SequenceLike[ColorLike], /) -> None:
        """Set the color palette for an 8-bit Surface.

        Set the full palette for an 8-bit Surface. This will replace the colors in
        the existing palette. A partial palette can be passed and only the first
        colors in the original palette will be changed.

        This function has no effect on a Surface with more than 8-bits per pixel.
        """

    def set_palette_at(self, index: int, color: ColorLike, /) -> None:
        """Set the color for a single index in an 8-bit Surface palette.

        Set the palette value for a single entry in a Surface palette. The index
        should be a value from 0 to 255.

        This function has no effect on a Surface with more than 8-bits per pixel.
        """

    def map_rgb(self, color: ColorLike, /) -> int:
        """Convert a color into a mapped color value.

        Convert a :data:`pygame.typing.ColorLike` into the mapped integer value
        for this Surface. The returned integer will contain no more bits than the
        bit depth of the Surface. Mapped color values are not often used inside pygame,
        but can be passed to most functions that require a Surface and a color.

        See the Surface object documentation for more information about colors
        and pixel formats.
        """

    def unmap_rgb(self, mapped_int: int, /) -> Color:
        """Convert a mapped integer color value into a Color.

        Convert an mapped integer color into the ``RGB`` color components for
        this Surface. Mapped color values are not often used inside pygame, but
        can be passed to most functions that require a Surface and a color.

        See the Surface object documentation for more information about colors
        and pixel formats.
        """

    def set_clip(self, rect: Optional[RectLike], /) -> None:
        """Set the current clipping area of the Surface.

        Each Surface has an active clipping area. This is a rectangle that
        represents the only pixels on the Surface that can be modified. If
        ``None`` is passed for the rectangle the full Surface will be available
        for changes.

        The clipping area is always restricted to the area of the Surface itself.
        If the clip rectangle is too large it will be shrunk to fit inside the
        Surface.
        """

    def get_clip(self) -> Rect:
        """Get the current clipping area of the Surface.

        Return a rectangle of the current clipping area. The Surface will always
        return a valid rectangle that will never be outside the bounds of the
        surface. If the Surface has had ``None`` set for the clipping area, the
        Surface will return a rectangle with the full area of the Surface.
        """

    @overload
    def subsurface(self, rect: RectLike, /) -> Surface: ...
    @overload
    def subsurface(self, left_top: Point, width_height: Point, /) -> Surface: ...
    @overload
    def subsurface(
        self, left: float, top: float, width: float, height: float, /
    ) -> Surface: ...
    def subsurface(self, *args):  # type: ignore
        """Create a new surface that references its parent.

        Returns a new Surface that shares its pixels with its new parent. The new
        Surface is considered a child of the original. Modifications to either
        Surface pixels will effect each other. Surface information like clipping
        area and color keys are unique to each Surface.

        The new Surface will inherit the palette, color key, and alpha settings
        from its parent.

        It is possible to have any number of subsurfaces and subsubsurfaces on
        the parent. It is also possible to subsurface the display Surface if the
        display mode is not hardware accelerated.

        See :meth:`get_offset()` and :meth:`get_parent()` to learn more
        about the state of a subsurface.

        A subsurface will have the same class as the parent surface.
        """

    def get_parent(self) -> Surface:
        """Find the parent of a subsurface.

        Returns the parent Surface of a subsurface. If this is not a subsurface
        then ``None`` will be returned.
        """

    def get_abs_parent(self) -> Surface:
        """Find the top level parent of a subsurface.

        Returns the parent Surface of a subsurface. If this is not a subsurface
        then this surface will be returned.
        """

    def get_offset(self) -> tuple[int, int]:
        """Find the position of a child subsurface inside a parent.

        Get the offset position of a child subsurface inside of a parent. If the
        Surface is not a subsurface this will return (0, 0).
        """

    def get_abs_offset(self) -> tuple[int, int]:
        """Find the absolute position of a child subsurface inside its top level parent.

        Get the offset position of a child subsurface inside of its top level
        parent Surface. If the Surface is not a subsurface this will return (0,
        0).
        """

    def get_size(self) -> tuple[int, int]:
        """Get the dimensions of the Surface.

        Return the width and height of the Surface in pixels. Can also be accessed
        with :attr:`size`
        """

    def get_width(self) -> int:
        """Get the width of the Surface.

        Return the width of the Surface in pixels. Can also be accessed with :attr:`width`
        """

    def get_height(self) -> int:
        """Get the height of the Surface.

        Return the height of the Surface in pixels. Can also be accessed with :attr:`height`
        """

    def get_rect(self, **kwargs: Any) -> Rect:
        """Get the rectangular area of the Surface.

        Returns a new rectangle covering the entire surface. This rectangle will
        always start at (0, 0) with a width and height the same size as the surface.

        You can pass keyword argument values to this function. These named values
        will be applied to the attributes of the Rect before it is returned. An
        example would be ``mysurf.get_rect(center=(100, 100))`` to create a
        rectangle for the Surface centered at a given position. Size attributes
        such as ``size`` or ``w`` can also be applied to resize the Rect.
        """

    def get_frect(self, **kwargs: Any) -> FRect:
        """Get the rectangular area of the Surface.

        This is the same as :meth:`Surface.get_rect` but returns an FRect. FRect is similar
        to Rect, except it stores float values instead.

        You can pass keyword argument values to this function. These named values
        will be applied to the attributes of the FRect before it is returned. An
        example would be ``mysurf.get_frect(center=(100.5, 100.5))`` to create a
        rectangle for the Surface centered at a given position. Size attributes
        such as ``size`` or ``w`` can also be applied to resize the FRect.

        ..versionadded:: 2.3.0
        """

    def get_bitsize(self) -> int:
        """Get the bit depth of the Surface pixel format.

        Returns the number of bits used to represent each pixel. This value may
        not exactly fill the number of bytes used per pixel. For example a 15 bit
        Surface still requires a full 2 bytes.
        """

    def get_bytesize(self) -> int:
        """Get the bytes used per Surface pixel.

        Return the number of bytes used per pixel.
        """

    def get_flags(self) -> int:
        """Get the additional flags used for the Surface.

        Returns a set of current Surface features. Each feature is a bit in the
        flags bitmask. Typical flags are ``RLEACCEL``, ``SRCALPHA``, and
        ``SRCCOLORKEY``.

        Here is a more complete list of flags. A full list can be found in
        ``SDL_video.h``

        ::

            SWSURFACE      0x00000000    # Surface is in system memory
            HWSURFACE      0x00000001    # (obsolete in pygame 2) Surface is in video memory
            ASYNCBLIT      0x00000004    # (obsolete in pygame 2) Use asynchronous blits if possible

        See :func:`pygame.display.set_mode()` for flags exclusive to the
        display surface.

        Used internally (read-only)

        ::

            HWACCEL        0x00000100    # Blit uses hardware acceleration
            SRCCOLORKEY    0x00001000    # Blit uses a source color key
            RLEACCELOK     0x00002000    # Private flag
            RLEACCEL       0x00004000    # Surface is RLE encoded
            SRCALPHA       0x00010000    # Blit uses source alpha blending
            PREALLOC       0x01000000    # Surface uses preallocated memory
        """

    def get_pitch(self) -> int:
        """Get the number of bytes used per Surface row.

        Return the number of bytes separating each row in the Surface. Surfaces
        in video memory are not always linearly packed. Subsurfaces will also
        have a larger pitch than their real width.

        This value is not needed for normal pygame usage.
        """

    def get_masks(self) -> tuple[int, int, int, int]:
        """The bitmasks needed to convert between a color and a mapped integer.

        Returns the bitmasks used to isolate each color in a mapped integer.

        This value is not needed for normal pygame usage.
        """

    @deprecated("since 2.0.0. Immutable in SDL2")
    def set_masks(self, color: ColorLike, /) -> None:
        """Set the bitmasks needed to convert between a color and a mapped integer.

        This is not needed for normal pygame usage.

        .. note:: Starting in pygame 2.0, the masks are read-only and
            accordingly this method will raise a TypeError if called.

        .. deprecatedold:: 2.0.0

        .. versionaddedold:: 1.8.1
        """

    def get_shifts(self) -> tuple[int, int, int, int]:
        """The bit shifts needed to convert between a color and a mapped integer.

        Returns the pixel shifts need to convert between each color and a mapped
        integer.

        This value is not needed for normal pygame usage.
        """

    @deprecated("since 2.0.0. Immutable in SDL2")
    def set_shifts(self, color: ColorLike, /) -> None:
        """Sets the bit shifts needed to convert between a color and a mapped integer.

        This is not needed for normal pygame usage.

        .. note:: Starting in pygame 2.0, the shifts are read-only and
            accordingly this method will raise a TypeError if called.

        .. deprecatedold:: 2.0.0

        .. versionaddedold:: 1.8.1
        """

    def get_losses(self) -> tuple[int, int, int, int]:
        """The significant bits used to convert between a color and a mapped integer.

        Return the least significant number of bits stripped from each color in a
        mapped integer.

        This value is not needed for normal pygame usage.
        """

    def get_bounding_rect(self, min_alpha: int = 1) -> Rect:
        """Find the smallest rect containing data.

        Returns the smallest rectangular region that contains all the pixels in
        the surface that have an alpha value greater than or equal to the minimum
        alpha value.

        This function will temporarily lock and unlock the Surface as needed.

        .. versionaddedold:: 1.8
        """

    def get_view(self, kind: _ViewKind = "2", /) -> BufferProxy:
        """Return a buffer view of the Surface's pixels.

        Return an object which exports a surface's internal pixel buffer as
        a C level array struct, Python level array interface or a C level
        buffer interface. The new buffer protocol is supported.

        The kind argument is the length 1 string '0', '1', '2', '3',
        'r', 'g', 'b', or 'a'. The letters are case insensitive;
        'A' will work as well. The argument can be either a Unicode or byte (char)
        string. The default is '2'.

        '0' returns a contiguous unstructured bytes view. No surface shape
        information is given. A ``ValueError`` is raised if the surface's pixels
        are discontinuous.

        '1' returns a (surface-width * surface-height) array of continuous
        pixels. A ``ValueError`` is raised if the surface pixels are
        discontinuous.

        '2' returns a (surface-width, surface-height) array of raw pixels.
        The pixels are surface-bytesize-d unsigned integers. The pixel format is
        surface specific. The 3 byte unsigned integers of 24 bit surfaces are
        unlikely accepted by anything other than other pygame functions.

        '3' returns a (surface-width, surface-height, 3) array of ``RGB`` color
        components. Each of the red, green, and blue components are unsigned
        bytes. Only 24-bit and 32-bit surfaces are supported. The color
        components must be in either ``RGB`` or ``BGR`` order within the pixel.

        'r' for red, 'g' for green, 'b' for blue, and 'a' for alpha return a
        (surface-width, surface-height) view of a single color component within a
        surface: a color plane. Color components are unsigned bytes. Both 24-bit
        and 32-bit surfaces support 'r', 'g', and 'b'. Only 32-bit surfaces with
        ``SRCALPHA`` support 'a'.

        The surface is locked only when an exposed interface is accessed.
        For new buffer interface accesses, the surface is unlocked once the
        last buffer view is released. For array interface and old buffer
        interface accesses, the surface remains locked until the BufferProxy
        object is released.

        .. versionaddedold:: 1.9.2
        """

    def get_buffer(self) -> BufferProxy:
        """Acquires a buffer object for the pixels of the Surface.

        Return a buffer object for the pixels of the Surface. The buffer can be
        used for direct pixel access and manipulation. Surface pixel data is
        represented as an unstructured block of memory, with a start address
        and length in bytes. The data need not be contiguous. Any gaps are
        included in the length, but otherwise ignored.

        This method implicitly locks the Surface. The lock will be released when
        the returned :mod:`pygame.BufferProxy` object is garbage collected.

        .. versionaddedold:: 1.8
        """

    def get_blendmode(self) -> int: ...
    @property
    def _pixels_address(self) -> int:
        """Pixel buffer address.

        The starting address of the surface's raw pixel bytes.

        .. versionaddedold:: 1.9.2
        """

    def premul_alpha(self) -> Surface:
        """Returns a copy of the surface with the RGB channels pre-multiplied by the alpha channel.

        Returns a copy of the initial surface with the red, green and blue color
        channels multiplied by the alpha channel. This is intended to make it
        easier to work with the BLEND_PREMULTIPLED blend mode flag of the blit()
        method. Surfaces which have called this method will only look correct
        after blitting if the BLEND_PREMULTIPLED special flag is used.

        It is worth noting that after calling this method, methods that return the
        color of a pixel such as get_at() will return the alpha multiplied color
        values. It is not possible to fully reverse an alpha multiplication of
        the colors in a surface as integer color channel data is generally
        reduced by the operation (e.g. 255 x 0 = 0, from there it is not
        possible to reconstruct the original 255 from just the two remaining
        zeros in the color and alpha channels).

        If you call this method, and then call it again, it will multiply the color
        channels by the alpha channel twice. There are many possible ways to obtain
        a surface with the color channels pre-multiplied by the alpha channel in
        pygame, and it is not possible to tell the difference just from the
        information in the pixels. It is completely possible to have two identical
        surfaces - one intended for pre-multiplied alpha blending and one intended
        for normal blending. For this reason we do not store state on surfaces
        intended for pre-multiplied alpha blending.

        Surfaces without an alpha channel cannot use this method and will return
        an error if you use it on them. It is best used on 32 bit surfaces (the
        default on most platforms) as the blitting on these surfaces can be
        accelerated by SIMD versions of the pre-multiplied blitter.

        In general pre-multiplied alpha blitting is faster then 'straight alpha'
        blitting and produces superior results when blitting an alpha surface onto
        another surface with alpha - assuming both surfaces contain pre-multiplied
        alpha colors.

        There is a `tutorial on premultiplied alpha blending here. <tutorials/en/premultiplied-alpha>`_

        .. versionadded:: 2.1.4
        """

    def premul_alpha_ip(self) -> Surface:
        """Multiplies the RGB channels by the surface alpha channel.

        Multiplies the RGB channels of the surface by the alpha channel in place
        and returns the surface.

        Surfaces without an alpha channel cannot use this method and will return
        an error if you use it on them. It is best used on 32 bit surfaces (the
        default on most platforms) as the blitting on these surfaces can be
        accelerated by SIMD versions of the pre-multiplied blitter.

        Refer to the :meth:`premul_alpha` method for more information.

        .. versionadded:: 2.5.1
        """

    @property
    def width(self) -> int:
        """Surface width in pixels (read-only).

        Read-only attribute. Same as :meth:`get_width()`

        .. versionadded:: 2.5.0
        """
    @property
    def height(self) -> int:
        """Surface height in pixels (read-only).

        Read-only attribute. Same as :meth:`get_height()`

        .. versionadded:: 2.5.0
        """

    @property
    def size(self) -> tuple[int, int]:
        """Surface size in pixels (read-only).

        Read-only attribute. Same as :meth:`get_size()`

        .. versionadded:: 2.5.0
        """

@deprecated("Use `Surface` instead (SurfaceType is an old alias)")
class SurfaceType(Surface): ...
