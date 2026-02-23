from typing import Literal, TypeAlias

import numpy
from pygame.surface import Surface

_Kind: TypeAlias = Literal["P", "p", "R", "r", "G", "g", "B", "b", "A", "a", "C", "c"]

def surface_to_array(
    array: numpy.ndarray,
    surface: Surface,
    kind: _Kind = "P",
    opaque: int = 255,
    clear: int = 0,
) -> None: ...
def array_to_surface(surface: Surface, array: numpy.ndarray, /) -> None: ...
def map_array(
    array1: numpy.ndarray, array2: numpy.ndarray, surface: Surface, /
) -> None: ...
def make_surface(array: numpy.ndarray, /) -> Surface: ...
