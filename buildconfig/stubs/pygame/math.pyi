"""Pygame module for vector classes.

The pygame math module currently provides Vector classes in two and three
dimensions, ``Vector2`` and ``Vector3`` respectively.

They support the following numerical operations: ``vec + vec``, ``vec - vec``,
``vec * number``, ``number * vec``, ``vec / number``, ``vec // number``, ``vec += vec``,
``vec -= vec``, ``vec *= number``, ``vec /= number``, ``vec //= number``, ``round(vec, ndigits=0)``.

All these operations will be performed elementwise.
In addition ``vec * vec`` will perform a scalar-product (a.k.a. dot-product).
If you want to multiply every element from vector v with every element from
vector w you can use the elementwise method: ``v.elementwise() * w``

The coordinates of a vector can be retrieved or set using attributes or
subscripts

::

   v = pygame.Vector3()

   v.x = 5
   v[1] = 2 * v.x
   print(v[1]) # 10

   v.x == v[0]
   v.y == v[1]
   v.z == v[2]

Multiple coordinates can be set and retrieved using slices or swizzling.

::

   v = pygame.Vector2()
   v.xy = 1, 2
   v[:] = 1, 2
   print(v)  # Vector2(1, 2)
   print(v.x)  # 1.0
   print(v.y)  # 2.0
   print(v.xy)  # Vector2(1, 2)
   print(v.yx)  # Vector2(2, 1)
   print(v.xyyx)  # (1.0, 2.0, 2.0, 1.0)

Note above, that swizzling with 2 components will return a Vector2 instance,
swizzling with 3 components will return a Vector3 instance, and swizzles of 4
or more components will result in a tuple. But since vectors support the
iterator protocol, they can be unpacked, or converted to lists or tuples.

::

   v = Vector2(1, 2)
   print(*v)  # 1.0 2.0
   print(tuple(v))  # (1.0, 2.0)
   print(tuple(v.yx))  # (2.0, 1.0)


A vector can be converted to other data types using the built-in constructors

::

    v = pygame.Vector2(1, 2)

    list(v) == [1.0, 2.0]
    tuple(v) == (1.0, 2.0)
    set(v) == {1.0, 2.0}

Conversion can be combined with swizzling or slicing to create a new order

::

    v = pygame.Vector3(1, 2, 3)

    list(v.xz) == [1.0, 3.0]
    list(v.zyx) == [3.0, 2.0, 1.0]
    list(v.yyy) == [2.0, 2.0, 2.0]
    tuple(v.xyyzzz) == (1.0, 2.0, 2.0, 3.0, 3.0, 3.0)
    tuple(v.zxyxzzyx) == (3.0, 1.0, 2.0, 1.0, 3.0, 3.0, 2.0, 1.0)
    set(v.yxzxzyzxyx) == {1.0, 2.0, 3.0} # sets remove duplicates

    list(v[:]) == [1.0, 2.0, 3.0]
    tuple(v[::-1]) == (3.0, 2.0, 1.0)
    set(v[1:3]) == {2.0, 3.0}

.. versionaddedold:: 1.9.2pre
.. versionchangedold:: 1.9.4 Removed experimental notice.
.. versionchangedold:: 1.9.4 Allow scalar construction like GLSL Vector2(2) == Vector2(2.0, 2.0)
.. versionchangedold:: 1.9.4 :mod:`pygame.math` import not required. More convenient ``pygame.Vector2`` and ``pygame.Vector3``.
.. versionchanged:: 2.1.4 `round` returns a new vector with components rounded to the specified digits.
"""

from collections.abc import Collection, Iterator
from typing import (
    Any,
    ClassVar,
    Generic,
    Literal,
    SupportsIndex,
    TypeVar,
    final,
    overload,
)

from pygame.typing import SequenceLike
from typing_extensions import deprecated  # added in 3.13

def clamp(value: float, min: float, max: float, /) -> float:
    """Returns value clamped to min and max.

    Clamps a numeric ``value`` so that it's no lower than ``min``, and no higher
    than ``max``.

    .. versionadded:: 2.1.3
    """

_TVec = TypeVar("_TVec", bound=_GenericVector)

# not implemented in code, only implemented here for ease of implementing
# typestubs. Contains attributes/methods common to Vector2 and Vector3
# Also used with _TVec generics
class _GenericVector(Collection[float]):
    epsilon: float
    __hash__: ClassVar[None]  # type: ignore[assignment]
    def __len__(self) -> int: ...
    @overload
    def __setitem__(self, key: int, value: float) -> None: ...
    @overload
    def __setitem__(self, key: slice, value: SequenceLike[float] | _TVec) -> None: ...
    @overload
    def __getitem__(self, i: SupportsIndex) -> float: ...
    @overload
    def __getitem__(self, s: slice) -> list[float]: ...
    def __iter__(self) -> VectorIterator: ...
    def __add__(self: _TVec, other: SequenceLike[float] | _TVec) -> _TVec: ...
    def __radd__(self: _TVec, other: SequenceLike[float] | _TVec) -> _TVec: ...
    def __sub__(self: _TVec, other: SequenceLike[float] | _TVec) -> _TVec: ...
    def __rsub__(self: _TVec, other: SequenceLike[float] | _TVec) -> _TVec: ...
    @overload
    def __mul__(self: _TVec, other: SequenceLike[float] | _TVec) -> float: ...
    @overload
    def __mul__(self: _TVec, other: float) -> _TVec: ...
    def __rmul__(self: _TVec, other: float) -> _TVec: ...
    def __truediv__(self: _TVec, other: float) -> _TVec: ...
    def __rtruediv__(self: _TVec, other: float) -> _TVec: ...
    def __floordiv__(self: _TVec, other: float) -> _TVec: ...
    def __neg__(self: _TVec) -> _TVec: ...
    def __pos__(self: _TVec) -> _TVec: ...
    def __bool__(self) -> bool: ...
    def __iadd__(self: _TVec, other: SequenceLike[float] | _TVec) -> _TVec: ...
    def __isub__(self: _TVec, other: SequenceLike[float] | _TVec) -> _TVec: ...
    @overload
    def __imul__(self: _TVec, other: SequenceLike[float] | _TVec) -> float: ...
    @overload
    def __imul__(self: _TVec, other: float) -> _TVec: ...
    def __copy__(self: _TVec) -> _TVec: ...
    def copy(self: _TVec) -> _TVec: ...
    def __contains__(self, other: float) -> bool: ...  # type: ignore[override]
    def dot(self: _TVec, other: SequenceLike[float] | _TVec, /) -> float: ...
    def magnitude(self) -> float: ...
    def magnitude_squared(self) -> float: ...
    def length(self) -> float: ...
    def length_squared(self) -> float: ...
    def normalize(self: _TVec) -> _TVec: ...
    def normalize_ip(self) -> None: ...
    def is_normalized(self) -> bool: ...
    def scale_to_length(self, value: float, /) -> None: ...
    def reflect(self: _TVec, other: SequenceLike[float] | _TVec, /) -> _TVec: ...
    def reflect_ip(self: _TVec, other: SequenceLike[float] | _TVec, /) -> None: ...
    def distance_to(self: _TVec, other: SequenceLike[float] | _TVec, /) -> float: ...
    def distance_squared_to(
        self: _TVec, other: SequenceLike[float] | _TVec, /
    ) -> float: ...
    def lerp(
        self: _TVec, other: SequenceLike[float] | _TVec, value: float, /
    ) -> _TVec: ...
    def slerp(
        self: _TVec, other: SequenceLike[float] | _TVec, value: float, /
    ) -> _TVec: ...
    def smoothstep(
        self: _TVec, other: SequenceLike[float] | _TVec, value: float, /
    ) -> _TVec: ...
    def elementwise(self: _TVec) -> VectorElementwiseProxy[_TVec]: ...
    def angle_to(self: _TVec, other: SequenceLike[float] | _TVec, /) -> float: ...
    def move_towards(
        self: _TVec, target: SequenceLike[float] | _TVec, max_distance: float, /
    ) -> _TVec: ...
    def move_towards_ip(
        self: _TVec, target: SequenceLike[float] | _TVec, max_distance: float, /
    ) -> None: ...
    @overload
    def clamp_magnitude(self: _TVec, max_length: float, /) -> _TVec: ...
    @overload
    def clamp_magnitude(
        self: _TVec, min_length: float, max_length: float, /
    ) -> _TVec: ...
    @overload
    def clamp_magnitude_ip(self, max_length: float, /) -> None: ...
    @overload
    def clamp_magnitude_ip(self, min_length: float, max_length: float, /) -> None: ...
    def project(self: _TVec, other: SequenceLike[float] | _TVec, /) -> _TVec: ...
    def __round__(self: _TVec, ndigits: int | None = None, /) -> _TVec: ...

# VectorElementwiseProxy is a generic, it can be an elementwiseproxy object for
# Vector2, Vector3 and vector subclass objects
@final
class VectorElementwiseProxy(Generic[_TVec]):
    def __add__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __radd__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __sub__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __rsub__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __mul__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __rmul__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __truediv__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __rtruediv__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __floordiv__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __rfloordiv__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __mod__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __rmod__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> _TVec: ...
    def __pow__(
        self,
        power: float | _TVec | VectorElementwiseProxy[_TVec],
        mod: None = None,
    ) -> _TVec: ...
    def __rpow__(
        self,
        power: float | _TVec | VectorElementwiseProxy[_TVec],
        mod: None = None,
    ) -> _TVec: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __gt__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> bool: ...
    def __lt__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> bool: ...
    def __ge__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> bool: ...
    def __le__(
        self,
        other: float | _TVec | VectorElementwiseProxy[_TVec],
    ) -> bool: ...
    def __abs__(self) -> _TVec: ...
    def __neg__(self) -> _TVec: ...
    def __pos__(self) -> _TVec: ...
    def __bool__(self) -> bool: ...

@final
class VectorIterator:
    def __length_hint__(self) -> int: ...
    def __iter__(self) -> Iterator[float]: ...
    def __next__(self) -> float: ...

class Vector2(_GenericVector):
    x: float
    y: float
    xx: Vector2
    xy: Vector2
    yx: Vector2
    yy: Vector2
    @property
    def angle(self) -> float: ...
    @property
    def angle_rad(self) -> float: ...
    @overload
    def __init__(
        self: _TVec,
        x: str | float | SequenceLike[float] | _TVec = 0,
    ) -> None: ...
    @overload
    def __init__(self, x: float, y: float) -> None: ...
    def __reduce__(self: _TVec) -> tuple[type[_TVec], tuple[float, float]]: ...
    def rotate(self: _TVec, angle: float, /) -> _TVec: ...
    def rotate_rad(self: _TVec, angle: float, /) -> _TVec: ...
    def rotate_ip(self, angle: float, /) -> None: ...
    def rotate_rad_ip(self, angle: float, /) -> None: ...
    @deprecated("since 2.1.1. Use `pygame.Vector2.rotate_rad_ip` instead")
    def rotate_ip_rad(self, angle: float, /) -> None: ...
    def cross(self: _TVec, other: SequenceLike[float] | _TVec, /) -> float: ...
    def as_polar(self) -> tuple[float, float]: ...
    def from_polar(self, polar_value: SequenceLike[float], /) -> None: ...
    @overload
    def update(
        self: _TVec,
        x: str | float | SequenceLike[float] | _TVec = 0,
    ) -> None: ...
    @overload
    def update(self, x: float = 0, y: float = 0) -> None: ...

class Vector3(_GenericVector):
    x: float
    y: float
    z: float
    xx: Vector2
    xy: Vector2
    xz: Vector2
    yx: Vector2
    yy: Vector2
    yz: Vector2
    zx: Vector2
    zy: Vector2
    zz: Vector2
    xxx: Vector3
    xxy: Vector3
    xxz: Vector3
    xyx: Vector3
    xyy: Vector3
    xyz: Vector3
    xzx: Vector3
    xzy: Vector3
    xzz: Vector3
    yxx: Vector3
    yxy: Vector3
    yxz: Vector3
    yyx: Vector3
    yyy: Vector3
    yyz: Vector3
    yzx: Vector3
    yzy: Vector3
    yzz: Vector3
    zxx: Vector3
    zxy: Vector3
    zxz: Vector3
    zyx: Vector3
    zyy: Vector3
    zyz: Vector3
    zzx: Vector3
    zzy: Vector3
    zzz: Vector3
    @overload
    def __init__(
        self: _TVec,
        x: str | float | SequenceLike[float] | _TVec = 0,
    ) -> None: ...
    @overload
    def __init__(self, x: float, y: float, z: float) -> None: ...
    def __reduce__(self: _TVec) -> tuple[type[_TVec], tuple[float, float, float]]: ...
    def cross(self: _TVec, other: SequenceLike[float] | _TVec, /) -> _TVec: ...
    def rotate(
        self: _TVec, angle: float, axis: SequenceLike[float] | _TVec, /
    ) -> _TVec: ...
    def rotate_rad(
        self: _TVec, angle: float, axis: SequenceLike[float] | _TVec, /
    ) -> _TVec: ...
    def rotate_ip(
        self: _TVec, angle: float, axis: SequenceLike[float] | _TVec, /
    ) -> None: ...
    def rotate_rad_ip(
        self: _TVec, angle: float, axis: SequenceLike[float] | _TVec, /
    ) -> None: ...
    @deprecated("since 2.1.1. Use `pygame.Vector3.rotate_rad_ip` instead")
    def rotate_ip_rad(
        self: _TVec, angle: float, axis: SequenceLike[float] | _TVec, /
    ) -> None: ...
    def rotate_x(self: _TVec, angle: float, /) -> _TVec: ...
    def rotate_x_rad(self: _TVec, angle: float, /) -> _TVec: ...
    def rotate_x_ip(self, angle: float, /) -> None: ...
    def rotate_x_rad_ip(self, angle: float, /) -> None: ...
    @deprecated("since 2.1.1. Use `pygame.Vector3.rotate_x_rad_ip` instead")
    def rotate_x_ip_rad(self, angle: float, /) -> None: ...
    def rotate_y(self: _TVec, angle: float, /) -> _TVec: ...
    def rotate_y_rad(self: _TVec, angle: float, /) -> _TVec: ...
    def rotate_y_ip(self, angle: float, /) -> None: ...
    def rotate_y_rad_ip(self, angle: float, /) -> None: ...
    @deprecated("since 2.1.1. Use `pygame.Vector3.rotate_y_rad_ip` instead")
    def rotate_y_ip_rad(self, angle: float, /) -> None: ...
    def rotate_z(self: _TVec, angle: float, /) -> _TVec: ...
    def rotate_z_rad(self: _TVec, angle: float, /) -> _TVec: ...
    def rotate_z_ip(self, angle: float, /) -> None: ...
    def rotate_z_rad_ip(self, angle: float, /) -> None: ...
    @deprecated("since 2.1.1. Use `pygame.Vector3.rotate_z_rad_ip` instead")
    def rotate_z_ip_rad(self, angle: float, /) -> None: ...
    def as_spherical(self) -> tuple[float, float, float]: ...
    def from_spherical(self, spherical: tuple[float, float, float], /) -> None: ...
    @overload
    def update(
        self: _TVec,
        x: str | float | SequenceLike[float] | _TVec = 0,
    ) -> None: ...
    @overload
    def update(self, x: float = 0, y: float = 0, z: float = 0) -> None: ...

def lerp(a: float, b: float, value: float, do_clamp: bool = True, /) -> float:
    """Returns value linearly interpolated between a and b.

    Returns a number which is a linear interpolation between ``a``
    and ``b``. The third parameter determines how far between ``a`` and
    ``b`` the result is going to be.
    If ``do_clamp`` is false, ``value`` is not clamped to ``[0, 1]``,
    allowing extrapolation outside the range ``[a, b]``.

    The formula is:

    ``a + (b - a) * value``.

    .. versionadded:: 2.4.0
    """

def invlerp(a: float, b: float, value: float, /) -> float:
    """Returns value inverse interpolated between a and b.

    Returns a number which is an inverse interpolation between ``a``
    and ``b``. The third parameter ``value`` is the result of the linear interpolation
    between a and b with a certain coefficient. In other words, this coefficient
    will be the result of this function.
    If ``b`` and ``a`` are equal, it raises a ``ValueError``.

    The formula is:

    ``(v - a)/(b - a)``.

    This is an example explaining what is above :

    .. code-block:: python

        >>> a = 10
        >>> b = 20
        >>> pygame.math.invlerp(10, 20, 11.5)
        0.15
        >>> pygame.math.lerp(10, 20, 0.15)
        11.5


    .. versionadded:: 2.5.0
    """

def smoothstep(a: float, b: float, value: float, /) -> float:
    """Returns value smoothly interpolated between a and b.

    Returns a number which is a smooth interpolation between ``a``
    and ``b``. This means that the interpolation follows an s-shaped curve, with
    change happening more slowly near the limits (0.0 and 1.0) and faster in the middle.
    The third parameter determines how far between ``a`` and
    ``b`` the result is going to be. Value is clamped to ``[0, 1]``.

    The formula is:

    ``a * (1 - interp) + b * interp``

    where:

    ``interp = value * value * (3 - 2 * value)``

    .. versionadded:: 2.4.0
    """

def remap(
    i_min: float, i_max: float, o_min: float, o_max: float, value: float, /
) -> float:
    """Remaps value from given input range to given output range.

    Returns a number which is the value remapped from ``[i_min, i_max]`` range to
    ``[o_min, o_max]`` range.
    If ``i_min`` and ``i_max`` are equal, it raises a ``ValueError``.

    Example:

    .. code-block:: python

        >>> value = 50
        >>> pygame.math.remap(0, 100, 0, 200, value)
        100.0


    .. versionadded:: 2.5.0
    """

@deprecated("Functionality is removed")
def enable_swizzling() -> None: ...
@deprecated("Functionality is removed")
def disable_swizzling() -> None: ...
