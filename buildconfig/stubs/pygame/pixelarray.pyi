from typing import Any, Dict, Tuple, Union, overload

from pygame.surface import Surface

from ._common import ColorValue, Sequence

class PixelArray:
    surface: Surface
    itemsize: int
    ndim: int
    shape: Tuple[int, ...]
    strides: Tuple[int, ...]
    # possibly going to be deprecated/removed soon, in which case these
    # typestubs must be removed too
    __array_interface__: Dict[str, Any]
    __array_struct__: Any
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
    def __getitem__(self, indices: Tuple[int, int]) -> int: ...
    # returns self
    @overload
    def __getitem__(self, ell: ellipsis) -> PixelArray: ...
    def make_surface(self) -> Surface: ...
    def replace(
        self,
        color: ColorValue,
        repcolor: ColorValue,
        distance: float = 0,
        weights: Sequence[float] = (0.299, 0.587, 0.114),
    ) -> None: ...
    def extract(
        self,
        color: ColorValue,
        distance: float = 0,
        weights: Sequence[float] = (0.299, 0.587, 0.114),
    ) -> PixelArray: ...
    def compare(
        self,
        array: PixelArray,
        distance: float = 0,
        weights: Sequence[float] = (0.299, 0.587, 0.114),
    ) -> PixelArray: ...
    def transpose(self) -> PixelArray: ...
    def close(self) -> PixelArray: ...
