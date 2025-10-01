from collections.abc import Callable, Hashable, Iterable
from typing import Optional, Union

from pygame.font import Font

def get_fonts() -> list[str]: ...
def match_font(
    name: Union[str, bytes, Iterable[Union[str, bytes]]],
    bold: Hashable = False,
    italic: Hashable = False,
) -> str: ...
def SysFont(
    name: Union[str, bytes, Iterable[Union[str, bytes]], None],
    size: int,
    bold: Hashable = False,
    italic: Hashable = False,
    constructor: Optional[Callable[[Optional[str], int, bool, bool], Font]] = None,
) -> Font: ...
