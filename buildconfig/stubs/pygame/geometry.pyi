from typing import (
    Sequence,
    overload, Tuple,
)

from ._common import Coordinate

class Circle:
    x: float
    y: float
    r: float
    radius: float
    r_sqr: float
    d: float
    diameter: float
    area: float
    circumference: float
    center: Tuple[float, float]

    @overload
    def __init__(self, x: float, y: float, r: float) -> None: ...
    @overload
    def __init__(self, pos: Coordinate, r: float) -> None: ...
    @overload
    def __init__(self, circle: Circle) -> None: ...
    @overload
    def __init__(self, obj_with_circle_attr) -> None: ...
    def __copy__(self) -> Circle: ...
    copy = __copy__
