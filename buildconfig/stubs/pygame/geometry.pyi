from typing import (
    Sequence,
    overload,
)

from pygame._common import Coordinate


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
    def __copy__(self) -> Circle: ...
    copy = __copy__
