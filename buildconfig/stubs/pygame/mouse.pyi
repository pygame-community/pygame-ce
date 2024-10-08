from typing import Literal, Tuple, overload
from typing_extensions import deprecated # added in 3.13

from pygame.cursors import Cursor
from pygame.surface import Surface

from pygame.typing import Point, SequenceLike, IntPoint

@overload
def get_pressed(
    num_buttons: Literal[3] = 3,
    desktop: bool = False) -> Tuple[bool, bool, bool]: ...
@overload
def get_pressed(
    num_buttons: Literal[5],
    desktop: bool = False) -> Tuple[bool, bool, bool, bool, bool]: ...
def get_just_pressed() -> Tuple[bool, bool, bool, bool, bool]: ...
def get_just_released() -> Tuple[bool, bool, bool, bool, bool]: ...
def get_pos(desktop: bool = False) -> Tuple[int, int]: ...
def get_rel() -> Tuple[int, int]: ...
@overload
def set_pos(pos: Point, /) -> None: ...
@overload
def set_pos(x: float, y: float, /) -> None: ...
def set_visible(value: bool, /) -> int: ...
def get_visible() -> bool: ...
def get_focused() -> bool: ...
@overload
def set_cursor(cursor: Cursor) -> None: ...
@overload
def set_cursor(constant: int) -> None: ...
@overload
def set_cursor(
    size: IntPoint,
    hotspot: IntPoint,
    xormasks: SequenceLike[int],
    andmasks: SequenceLike[int],
) -> None: ...
@overload
def set_cursor(hotspot: IntPoint, surface: Surface) -> None: ...
def get_cursor() -> Cursor: ...
@deprecated("since 2.2.0. Use `pygame.mouse.set_cursor` instead")
def set_system_cursor(cursor: int, /) -> None: ...
def get_relative_mode() -> bool: ...
def set_relative_mode(enable: bool, /) -> None: ...
