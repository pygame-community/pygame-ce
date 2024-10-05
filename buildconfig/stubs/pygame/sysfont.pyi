from typing import Callable, Hashable, Iterable, List, Optional, Union

from pygame.font import Font

def get_fonts() -> List[str]: ...
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
