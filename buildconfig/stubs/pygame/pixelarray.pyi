import sys
from typing import Any, Union, overload

from pygame.color import Color
from pygame.surface import Surface
from pygame.typing import SequenceLike

# 'ellipsis' existed in typeshed pre 3.10, now we use EllipsisType which is
# the modern standard library equivalent.
if sys.version_info >= (3, 10):
    from types import EllipsisType
else:
    EllipsisType = ellipsis

_PixelColor = Union[int, Color, tuple[int, int, int], tuple[int, int, int, int]]

class PixelArray:
    @property
    def surface(self) -> Surface: ...
    @property
    def itemsize(self) -> int: ...
    @property
    def ndim(self) -> int: ...
    @property
    def shape(self) -> tuple[int, ...]: ...
    @property
    def strides(self) -> tuple[int, ...]: ...
    # possibly going to be deprecated/removed soon, in which case these
    # typestubs must be removed too
    @property
    def __array_interface__(self) -> dict[str, Any]: ...
    @property
    def __array_struct__(self) -> Any: ...
    if sys.version_info >= (3, 12):
        def __buffer__(self, flags: int, /) -> memoryview[int]: ...
    def __init__(self, surface: Surface) -> None: ...
    def __enter__(self) -> PixelArray: ...
    def __exit__(self, *args, **kwargs) -> None: ...
    # if indexing into a 2D PixelArray, a 1D PixelArray will be returned
    # if indexing into a 1D PixelArray, an int will be returned
    @overload
    def __getitem__(self, index: int) -> Union[PixelArray, int]: ...
    # complicated, but I'm pretty sure this is guaranteed to return a PixelArray or None
    # will only return None if the slice start and end are the same
    @overload
    def __getitem__(self, index_range: slice) -> Union[PixelArray, None]: ...
    # only valid for a 2D PixelArray
    @overload
    def __getitem__(self, indices: tuple[int, int]) -> int: ...
    # returns self
    @overload
    def __getitem__(self, ell: EllipsisType) -> PixelArray: ...
    def make_surface(self) -> Surface: ...
    def replace(
        self,
        color: _PixelColor,
        repcolor: _PixelColor,
        distance: float = 0,
        weights: SequenceLike[float] = (0.299, 0.587, 0.114),
    ) -> None: ...
    def extract(
        self,
        color: _PixelColor,
        distance: float = 0,
        weights: SequenceLike[float] = (0.299, 0.587, 0.114),
    ) -> PixelArray: ...
    def compare(
        self,
        array: PixelArray,
        distance: float = 0,
        weights: SequenceLike[float] = (0.299, 0.587, 0.114),
    ) -> PixelArray: ...
    def transpose(self) -> PixelArray: ...
    def close(self) -> None: ...
