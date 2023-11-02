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
    Vector3,
    Circle,
    Tuple[float, float, float],
    Tuple[Tuple[float, float], float],
    Sequence[float],
]

class _HasCirclettribute(Protocol):
    # An object that has a circle attribute that is either a circle, or a function
    # that returns a circle
    circle: Union[CircleValue, Callable[[], CircleValue]]

CircleValue = Union[_CanBeCircle, _HasCirclettribute]

class Circle:
    x: float
    y: float
    r: float

    @overload
    def __init__(self, x: float, y: float, r: float) -> None: ...
    @overload
    def __init__(self, pos: Sequence[float], r: float) -> None: ...
    @overload
    def __init__(self, circle: Circle) -> None: ...
    @overload
    def __init__(self, obj_with_circle_attr) -> None: ...
    @overload
    def collidepoint(self, x: float, y: float) -> bool: ...
    @overload
    def collidepoint(self, point: Coordinate) -> bool: ...
    @overload
    def collidecircle(self, circle: CircleValue) -> bool: ...
    @overload
    def collidecircle(self, x: float, y: float, r: float) -> bool: ...
    def __copy__(self) -> Circle: ...
    copy = __copy__
