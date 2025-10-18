from collections.abc import Iterator
from typing import Any, Literal, TypeAlias, overload

from pygame.surface import Surface
from pygame.typing import FileLike, IntPoint, SequenceLike

_SmallString: TypeAlias = tuple[
    str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str
]
_BigString: TypeAlias = tuple[
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
]

arrow: Cursor
diamond: Cursor
broken_x: Cursor
tri_left: Cursor
tri_right: Cursor
ball: Cursor
thickarrow_strings: _BigString
sizer_x_strings: _SmallString
sizer_y_strings: _BigString
sizer_xy_strings: _SmallString
textmarker_strings: _SmallString

def compile(
    strings: SequenceLike[str],
    black: str = "X",
    white: str = ".",
    xor: str = "o",
) -> tuple[tuple[int, ...], tuple[int, ...]]: ...
def load_xbm(
    curs: FileLike, mask: FileLike
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, ...], tuple[int, ...]]: ...

class Cursor:
    @overload
    def __init__(self, constant: int = ...) -> None: ...
    @overload
    def __init__(self, cursor: Cursor) -> None: ...
    @overload
    def __init__(
        self,
        size: IntPoint,
        hotspot: IntPoint,
        xormasks: SequenceLike[int],
        andmasks: SequenceLike[int],
    ) -> None: ...
    @overload
    def __init__(
        self,
        hotspot: IntPoint,
        surface: Surface,
    ) -> None: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __len__(self) -> int: ...
    def __copy__(self) -> Cursor: ...
    def __hash__(self) -> int: ...
    def __getitem__(self, index: int) -> int | IntPoint | Surface: ...
    def copy(self) -> Cursor: ...
    type: Literal["system", "color", "bitmap"]
    data: (
        tuple[int]
        | tuple[tuple[int, int], tuple[int, int], tuple[int, ...], tuple[int, ...]]
        | tuple[IntPoint, Surface]
    )
