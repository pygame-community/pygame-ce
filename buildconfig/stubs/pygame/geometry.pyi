from typing import (
    Sequence,
    overload,
    Union,
    Callable,
    Protocol,
    Tuple,
)

from pygame import Vector3
from pygame._common import Coordinate

_CanBeCircle = Union[
    Circle,
    Tuple[float, float, float],
    Tuple[Tuple[float, float], float],
    Sequence[float],
    Vector3,
]

class _HasCirclettribute(Protocol):
    # An object that has a circle attribute that is either a circle, or a function
    # that returns a circle
    circle: Union[_CanBeCircle, Callable[[], _CanBeCircle]]

_CircleValue = Union[_CanBeCircle, _HasCirclettribute]

class Circle:
    x: float
    y: float
    r: float

    @overload
    def __init__(self, x: float, y: float, r: float) -> None: ...
    @overload
    def __init__(self, pos: Sequence[float], r: float) -> None: ...
    @overload
    def __init__(self, circle: _CircleValue) -> None: ...
    @overload
    def __init__(self, obj_with_circle_attr) -> None: ...
    @overload
    def collidepoint(self, x: float, y: float) -> bool: ...
    @overload
    def collidepoint(self, point: Coordinate) -> bool: ...
    @overload
    def collidecircle(self, circle: _CircleValue) -> bool: ...
    @overload
    def collidecircle(self, x: float, y: float, r: float) -> bool: ...
    def __copy__(self) -> Circle: ...
    copy = __copy__
