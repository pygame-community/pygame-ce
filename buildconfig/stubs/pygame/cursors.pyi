from collections.abc import Iterator
from typing import Any, Literal, Union, overload

from pygame.surface import Surface

from pygame.typing import FileLike, IntPoint, SequenceLike

_Small_string = tuple[
    str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str
]
_Big_string = tuple[
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
thickarrow_strings: _Big_string
sizer_x_strings: _Small_string
sizer_y_strings: _Big_string
sizer_xy_strings: _Small_string
textmarker_strings: _Small_string

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
    def __getitem__(
        self, index: int
    ) -> Union[int, IntPoint, Surface]: ...
    def copy(self) -> Cursor: ...
    type: Literal["system", "color", "bitmap"]
    data: Union[
        tuple[int],
        tuple[tuple[int, int], tuple[int, int], tuple[int, ...], tuple[int, ...]],
        tuple[IntPoint, Surface],
    ]
