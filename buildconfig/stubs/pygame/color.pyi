import sys
from collections.abc import Collection, Iterator
from typing import Any, ClassVar, SupportsIndex, overload

from pygame.typing import ColorLike
from typing_extensions import deprecated  # added in 3.13

THECOLORS: dict[str, tuple[int, int, int, int]]

# Color confirms to the Collection ABC, since it also confirms to
# Sized, Iterable and Container ABCs
class Color(Collection[int]):
    """Pygame object for color representations.

    The ``Color`` class represents ``RGBA`` color values using a value range of
    0 to 255 inclusive. It allows basic arithmetic operations — binary
    operations ``+``, ``-``, ``*``, ``//``, ``%``, and unary operation ``~`` — to
    create new colors, supports conversions to other color spaces such as ``HSV``
    or ``HSL`` and lets you adjust single color channels.
    Alpha defaults to 255 (fully opaque) when not given.
    The arithmetic operations and ``correct_gamma()`` method preserve subclasses.
    For the binary operators, the class of the returned color is that of the
    left hand color object of the operator.

    Color objects support swizzling for their ``RGBA`` attributes, which allows
    the creation of new color objects with the corresponding swizzled attributes
    as its ``RGBA`` attributes. For example, ``color.bgra`` provides a shortcut to
    doing ``Color(color.b, color.g, color.r, color.a)``. Swizzling with other than
    4 attributes will return a tuple consisting of the corresponding elements
    instead of a color object.

    Color objects support equality comparison with other color objects and 3 or
    4 element tuples of integers. There was a bug in pygame 1.8.1
    where the default alpha was 0, not 255 like previously.

    Color objects export the C level array interface. The interface exports a
    read-only one dimensional unsigned byte array of the same assigned length
    as the color. The new buffer interface is also exported, with the same
    characteristics as the array interface.

    The floor division, ``//``, and modulus, ``%``, operators do not raise
    an exception for division by zero. Instead, if a color, or alpha, channel
    in the right hand color is 0, then the result is 0. For example: ::

        # These expressions are True
        Color(255, 255, 255, 255) // Color(0, 64, 64, 64) == Color(0, 3, 3, 3)
        Color(255, 255, 255, 255) % Color(64, 64, 64, 0) == Color(63, 63, 63, 0)

    Use ``int(color)`` to return the immutable integer value of the color,
    usable as a ``dict`` key. This integer value differs from the mapped
    pixel values of :meth:`pygame.Surface.get_at_mapped`,
    :meth:`pygame.Surface.map_rgb` and :meth:`pygame.Surface.unmap_rgb`.
    It can be passed as a ``color_value`` argument to :class:`Color`
    (useful with sets).

    See :doc:`color_list` for samples of the available named colors.

    :param int r: red value in the range of 0 to 255 inclusive
    :param int g: green value in the range of 0 to 255 inclusive
    :param int b: blue value in the range of 0 to 255 inclusive
    :param int a: (optional) alpha value in the range of 0 to 255 inclusive,
        default is 255
    :param color_value: color value (see note below for the supported formats)

        .. note::
            Supported ``color_value`` formats:

            | - **Color object:** clones the given :class:`Color` object

            | - **Color name: str:** name of the color to use, e.g. ``'red'``
                (all the supported name strings can be found in the
                :doc:`color_list`, with sample swatches)

            | - **HTML color format str:** ``'#rrggbbaa'`` or ``'#rrggbb'``,
                where rr, gg, bb, and aa are 2-digit hex numbers in the range
                of 0 to 0xFF inclusive, the aa (alpha) value defaults to 0xFF
                if not provided

            | - **hex number str:** ``'0xrrggbbaa'`` or ``'0xrrggbb'``, where
                rr, gg, bb, and aa are 2-digit hex numbers in the range of 0x00
                to 0xFF inclusive, the aa (alpha) value defaults to 0xFF if not
                provided

            | - **int:** int value of the color to use, using hex numbers can
                make this parameter more readable, e.g. ``0xrrggbbaa``, where rr,
                gg, bb, and aa are 2-digit hex numbers in the range of 0x00 to
                0xFF inclusive, note that the aa (alpha) value is not optional for
                the int format and must be provided

            | - **tuple/list of int color values:** ``(R, G, B, A)`` or
                ``(R, G, B)``, where R, G, B, and A are int values in the range of
                0 to 255 inclusive, the A (alpha) value defaults to 255 if not
                provided

    :type color_value: Color or str or int or tuple(int, int, int, [int]) or
        list(int, int, int, [int])

    :returns: a newly created :class:`Color` object
    :rtype: Color

    .. versionchanged:: 2.5.6
        ``bytes(Color(...))`` (assuming `bytes <https://docs.python.org/3/library/stdtypes.html#bytes>`_ is
        the built-in type) now returns a ``bytes`` object (of length 4) with the RGBA values of the color,
        as opposed to :class:`Color` being interpreted as an integer (think ``int(Color(...))``) causing it
        to return a ``bytes`` object filled with 0s the length of said integer.
    .. versionchangedold:: 2.0.0
        Support for tuples, lists, and :class:`Color` objects when creating
        :class:`Color` objects.
    .. versionchangedold:: 1.9.2 Color objects export the C level array interface.
    .. versionchangedold:: 1.9.0 Color objects support 4-element tuples of integers.
    .. versionchangedold:: 1.8.1 New implementation of the class.
    """

    r: int
    """Gets or sets the red value of the Color.

    The red value of the Color.
    """

    g: int
    """Gets or sets the green value of the Color.

    The green value of the Color.
    """

    b: int
    """Gets or sets the blue value of the Color.

    The blue value of the Color.
    """

    a: int
    """Gets or sets the alpha value of the Color.

    The alpha value of the Color.
    """

    cmy: tuple[float, float, float]
    """Gets or sets the CMY representation of the Color.

    The ``CMY`` representation of the Color. The ``CMY`` components are in
    the ranges ``C`` = [0, 1], ``M`` = [0, 1], ``Y`` = [0, 1]. Note that this
    will not return the absolutely exact ``CMY`` values for the set ``RGB``
    values in all cases. Due to the ``RGB`` mapping from 0-255 and the
    ``CMY`` mapping from 0-1 rounding errors may cause the ``CMY`` values to
    differ slightly from what you might expect.
    """

    hsva: tuple[float, float, float, float]
    """Gets or sets the HSVA representation of the Color.

    The ``HSVA`` representation of the Color. The ``HSVA`` components are in
    the ranges ``H`` = [0, 360], ``S`` = [0, 100], ``V`` = [0, 100], A = [0,
    100]. Note that this will not return the absolutely exact ``HSV`` values
    for the set ``RGB`` values in all cases. Due to the ``RGB`` mapping from
    0-255 and the ``HSV`` mapping from 0-100 and 0-360 rounding errors may
    cause the ``HSV`` values to differ slightly from what you might expect.
    """

    hsla: tuple[float, float, float, float]
    """Gets or sets the HSLA representation of the Color.

    The ``HSLA`` representation of the Color. The ``HSLA`` components are in
    the ranges ``H`` = [0, 360], ``S`` = [0, 100], ``L`` = [0, 100], A = [0,
    100]. Note that this will not return the absolutely exact ``HSL`` values
    for the set ``RGB`` values in all cases. Due to the ``RGB`` mapping from
    0-255 and the ``HSL`` mapping from 0-100 and 0-360 rounding errors may
    cause the ``HSL`` values to differ slightly from what you might expect.
    """

    i1i2i3: tuple[float, float, float]
    """Gets or sets the I1I2I3 representation of the Color.

    The ``I1I2I3`` representation of the Color. The ``I1I2I3`` components are
    in the ranges ``I1`` = [0, 1], ``I2`` = [-0.5, 0.5], ``I3`` = [-0.5,
    0.5]. Note that this will not return the absolutely exact ``I1I2I3``
    values for the set ``RGB`` values in all cases. Due to the ``RGB``
    mapping from 0-255 and the ``I1I2I3`` mapping from 0-1 rounding errors
    may cause the ``I1I2I3`` values to differ slightly from what you might
    expect.
    """

    normalized: tuple[float, float, float, float]
    """Gets or sets the normalized representation of the Color.

    The ``Normalized`` representation of the Color. The components of the ``Normalized``
    representation represent the basic ``RGBA`` values but normalized the
    ranges of the values are ``r`` = [0, 1], ``g`` = [0, 1], ``b`` = [0, 1]
    and ``a`` = [0, 1] respectively. Note that this will not return the absolutely exact
    ``Normalized`` values for the set ``RGBA`` values in all cases.
    Due to the ``RGB`` mapping from 0-255 and the ``Normalized`` mapping from 0-1
    rounding errors may cause the ``Normalized`` values to differ
    slightly from what you might expect.

    .. versionadded:: 2.5.0
    """

    hex: str
    """Gets or sets the stringified hexadecimal representation of the Color.

    The stringified hexadecimal representation of the Color. The hexadecimal string
    is formatted as ``"#rrggbbaa"`` where rr, gg, bb, and aa are two digit hex numbers
    in the range from 0x00 to 0xff.

    Setting this property means changing the color channels in place. Both lowercase
    and uppercase letters are allowed, the alpha can be omitted (defaults to 0xff) and
    the string can start with either ``#`` or ``0x``.

    .. versionadded:: 2.5.4
    """

    __hash__: ClassVar[None]  # type: ignore[assignment]
    @property
    def __array_struct__(self) -> Any: ...
    if sys.version_info >= (3, 12):
        def __buffer__(self, flags: int, /) -> memoryview[int]: ...

    @overload
    def __init__(self, r: int, g: int, b: int, a: int = 255) -> None: ...
    @overload
    def __init__(self, rgbvalue: ColorLike) -> None: ...
    @overload
    def __getitem__(self, i: SupportsIndex) -> int: ...
    @overload
    def __getitem__(self, s: slice) -> tuple[int, ...]: ...
    def __setitem__(self, key: int, value: int) -> None: ...
    def __iter__(self) -> Iterator[int]: ...
    def __add__(self, other: Color) -> Color: ...
    def __sub__(self, other: Color) -> Color: ...
    def __mul__(self, other: Color) -> Color: ...
    def __floordiv__(self, other: Color) -> Color: ...
    def __mod__(self, other: Color) -> Color: ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __bytes__(self) -> bytes: ...
    def __len__(self) -> int: ...
    def __index__(self) -> int: ...
    def __invert__(self) -> Color: ...
    def __contains__(self, other: int) -> bool: ...  # type: ignore[override]
    def __getattribute__(self, name: str) -> Color | tuple[int, ...]: ...
    def __setattr__(self, name: str, value: Color | tuple[int, ...]) -> None: ...
    @overload
    @classmethod
    def from_cmy(cls, object: tuple[float, float, float], /) -> Color: ...
    @overload
    @classmethod
    def from_cmy(cls, c: float, m: float, y: float, /) -> Color: ...
    @classmethod  # type: ignore
    def from_cmy(cls, *args) -> Color:  # type: ignore
        """Returns a Color object from a CMY representation.

        Creates a Color object from the given CMY components. Refer to :attr:`Color.cmy`
        for more information.

        .. versionadded:: 2.3.1
        """

    @overload
    @classmethod
    def from_hsva(cls, object: tuple[float, float, float, float], /) -> Color: ...
    @overload
    @classmethod
    def from_hsva(cls, h: float, s: float, v: float, a: float, /) -> Color: ...
    @classmethod  # type: ignore
    def from_hsva(cls, *args) -> Color:  # type: ignore
        """Returns a Color object from an HSVA representation.

        Creates a Color object from the given HSVA components. Refer to :attr:`Color.hsva`
        for more information.

        .. versionadded:: 2.3.1
        """

    @overload
    @classmethod
    def from_hsla(cls, object: tuple[float, float, float, float], /) -> Color: ...
    @overload
    @classmethod
    def from_hsla(cls, h: float, s: float, l: float, a: float, /) -> Color: ...
    @classmethod  # type: ignore
    def from_hsla(cls, *args) -> Color:  # type: ignore
        """Returns a Color object from an HSLA representation.

        Creates a Color object from the given HSLA components. Refer to :attr:`Color.hsla`
        for more information.

        .. versionadded:: 2.3.1
        """

    @overload
    @classmethod
    def from_i1i2i3(cls, object: tuple[float, float, float], /) -> Color: ...
    @overload
    @classmethod
    def from_i1i2i3(cls, i1: float, i2: float, i3: float, /) -> Color: ...
    @classmethod  # type: ignore
    def from_i1i2i3(cls, *args) -> Color:  # type: ignore
        """Returns a Color object from a I1I2I3 representation.

        Creates a Color object from the given I1I2I3 components. Refer to :attr:`Color.i1i2i3`
        for more information.

        .. versionadded:: 2.3.1
        """

    @overload
    @classmethod
    def from_normalized(cls, object: tuple[float, float, float, float], /) -> Color: ...
    @overload
    @classmethod
    def from_normalized(cls, r: float, g: float, b: float, a: float, /) -> Color: ...
    @classmethod  # type: ignore
    def from_normalized(cls, *args) -> Color:  # type: ignore
        """Returns a Color object from a Normalized representation.

        Creates a Color object from the given Normalized components. Refer to :attr:`Color.normalized`
        for more information.

        .. versionadded:: 2.5.0
        """

    @classmethod
    def from_hex(cls, hex: str, /) -> Color:
        """Returns a Color object from a Hexadecimal representation.

        Creates a Color object from the given Hexadecimal components. Refer to :attr:`Color.hex`
        for more information.

        .. versionadded:: 2.5.6
        """

    def normalize(self) -> tuple[float, float, float, float]:
        """Returns the normalized RGBA values of the Color.

        Returns the normalized ``RGBA`` values of the Color as floating point
        values.
        """

    def correct_gamma(self, gamma: float, /) -> Color:
        """Applies a certain gamma value to the Color.

        Applies a certain gamma value to the Color and returns a new Color with
        the adjusted ``RGBA`` values.
        """

    @deprecated("since 2.1.3. Use unpacking instead")
    def set_length(self, length: int, /) -> None:
        """Set the number of elements in the Color to 1,2,3, or 4.

        DEPRECATED: You may unpack the values you need like so,
        ``r, g, b, _ = pygame.Color(100, 100, 100)``
        If you only want r, g and b
        Or
        ``r, g, *_ = pygame.Color(100, 100, 100)``
        if you only want r and g

        The default Color length is 4. Colors can have lengths 1,2,3 or 4. This
        is useful if you want to unpack to r,g,b and not r,g,b,a. If you want to
        get the length of a Color do ``len(acolor)``.

        .. deprecated:: 2.1.3
        .. versionaddedold:: 1.9.0
        """

    def grayscale(self) -> Color:
        """Returns the grayscale of a Color.

        Returns a new Color object which represents the grayscaled version of self, using the luminosity formula,
        which weights red, green, and blue according to their relative contribution to perceived brightness.

        .. versionadded:: 2.1.4
        """

    def lerp(self, color: ColorLike, amount: float) -> Color:
        """Returns a linear interpolation to the given Color.

        Returns a Color which is a linear interpolation between self and the
        given Color in RGBA space. The second parameter determines how far
        between self and other the result is going to be.
        It must be a value between 0 and 1 where 0 means self and 1 means
        other will be returned.

        .. versionaddedold:: 2.0.1
        """

    def premul_alpha(self) -> Color:
        """Returns a Color where the r,g,b components have been multiplied by the alpha.

        Returns a new Color where each of the red, green and blue color
        channels have been multiplied by the alpha channel of the original
        color. The alpha channel remains unchanged.

        This is useful when working with the ``BLEND_PREMULTIPLIED`` blending mode
        flag for :meth:`pygame.Surface.blit()`, which assumes that all surfaces using
        it are using pre-multiplied alpha colors.

        .. versionaddedold:: 2.0.0
        """

    @overload
    def update(self, r: int, g: int, b: int, a: int = 255, /) -> None: ...
    @overload
    def update(self, rgbvalue: ColorLike, /) -> None: ...
    def update(self, *args) -> None:  # type: ignore
        """Sets the elements of the color.

        Sets the elements of the color. See parameters for :meth:`pygame.Color` for the
        parameters of this function. If the alpha value was not set it will not change.

        .. versionaddedold:: 2.0.1
        """
