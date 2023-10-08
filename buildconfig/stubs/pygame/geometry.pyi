from typing import (
    Sequence,
    overload,
)

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
    def __copy__(self) -> Circle: ...
    copy = __copy__
