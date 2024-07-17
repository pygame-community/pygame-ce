import sys
from typing import IO, Callable, Tuple, Union, TypeVar, Protocol, SupportsIndex

if sys.version_info > (3, 9):
    from os import PathLike as _PathProtocol
else:
    _T = TypeVar("_T", bound=Union[str, bytes])

    class _PathProtocol(Protocol[_T]):
        def __fspath__(self) -> _T: ...


# For functions that take a file name
PathLike = Union[str, bytes, _PathProtocol[str], _PathProtocol[bytes]]
# Most pygame functions that take a file argument should be able to handle a FileLike type
FileLike = Union[PathLike, IO[bytes], IO[str]]

_T_co = TypeVar("_T_co", covariant=True)


class SequenceLike(Protocol[_T_co]):
    """
    Variant of the standard `Sequence` ABC that only requires `__getitem__` and `__len__`.
    """

    def __getitem__(self, __i: SupportsIndex) -> _T_co: ...
    def __len__(self) -> int: ...


# Modify typehints when it is possible to annotate sizes

# Pygame handles float without errors in most cases where a coordinate is expected,
# usually rounding to int. Also, 'Union[int, float] == float'
Coordinate = SequenceLike[float]
# This is used where ints are strictly required
IntCoordinate = SequenceLike[int]

# Used for functions that return an RGBA tuple
RGBATuple = Tuple[int, int, int, int]
ColorLike = Union[int, str, SequenceLike[int]]

_CanBeRect = SequenceLike[Union[float, Coordinate]]


class _HasRectAttribute(Protocol):
    # An object that has a rect attribute that is either a rect, or a function
    # that returns a rect confirms to the rect protocol
    rect: Union["RectLike", Callable[[], "RectLike"]]


RectLike = Union[_CanBeRect, _HasRectAttribute]
