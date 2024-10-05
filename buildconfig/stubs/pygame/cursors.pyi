from typing import Any, Iterator, Literal, Tuple, Union, overload

from pygame.surface import Surface

from pygame.typing import FileLike, IntPoint, SequenceLike

_Small_string = Tuple[
    str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str
]
_Big_string = Tuple[
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
) -> Tuple[Tuple[int, ...], Tuple[int, ...]]: ...
def load_xbm(
    curs: FileLike, mask: FileLike
) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, ...], Tuple[int, ...]]: ...

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
        Tuple[int],
        Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, ...], Tuple[int, ...]],
        Tuple[IntPoint, Surface],
    ]
