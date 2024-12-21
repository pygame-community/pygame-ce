"""Set of common pygame type aliases for proper typehint annotations"""

# NOTE: `src_py/typing.py` and `buildconfig/stubs/pygame/typing.pyi` must be duplicates.
# Use the command `python buildconfig/stubs/gen_stubs.py` to copy typing.py to typing.pyi

__all__ = [
    "RectLike",
    "SequenceLike",
    "FileLike",
    "ColorLike",
    "Point",
    "IntPoint",
]

from abc import abstractmethod
from collections.abc import Callable
from os import PathLike as _PathProtocol
from typing import IO, Union, Optional, TypeVar, Protocol, Any, Iterable

from pygame.color import Color
from pygame.rect import Rect, FRect


# For functions that take a file name
_PathLike = Union[str, bytes, _PathProtocol[str], _PathProtocol[bytes]]
# Most pygame functions that take a file argument should be able to handle a FileLike type
FileLike = Union[_PathLike, IO[bytes], IO[str]]

_T_co = TypeVar("_T_co", covariant=True)


class SequenceLike(Protocol[_T_co]):
    """
    Variant of the standard `Sequence` ABC that only requires `__getitem__`.
    """

    @abstractmethod
    def __getitem__(self, index: int, /) -> _T_co: ...


IterableLike = Union[SequenceLike[_T_co], Iterable[_T_co]]


# Modify typehints when it is possible to annotate sizes

# Pygame handles float without errors in most cases where a point is expected,
# usually rounding to int. Also, 'Union[int, float] == float'
Point = SequenceLike[float]
# This is used where ints are strictly required
IntPoint = SequenceLike[int]

ColorLike = Union[Color, SequenceLike[int], str, int]


class _HasRectAttribute(Protocol):
    # An object that has a rect attribute that is either a rect, or a function
    # that returns a rect conforms to the rect protocol
    @property
    def rect(self) -> Union["RectLike", Callable[[], "RectLike"]]: ...


RectLike = Union[
    Rect, FRect, SequenceLike[float], SequenceLike[Point], _HasRectAttribute
]


class EventLike(Protocol):
    type: int

    def __init__(
        self, dict: Optional[dict[str, Any]] = None, **kwargs: Any
    ) -> None: ...

    @property
    def dict(self) -> dict[str, Any]: ...


# cleanup namespace
del (
    abstractmethod,
    Color,
    Rect,
    FRect,
    IO,
    Callable,
    Union,
    Optional,
    TypeVar,
    Protocol,
    Any,
)
