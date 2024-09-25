"""Set of common pygame type aliases for proper typehint annotations"""

# NOTE: `src_py/typing.py` and `buildconfig/stubs/pygame/typing.pyi` must be duplicates.
# Use the command `python buildconfig/stubs/gen_stubs.py` to copy typing.py to typing.pyi

__all__ = [
    "RectLike",
    "SequenceLike",
    "FileLike",
    "ColorLike",
    "Coordinate",
    "IntCoordinate",
]

import sys
from abc import abstractmethod
from typing import IO, Any, Callable, Dict, Optional, Tuple, Union, TypeVar, Protocol

if sys.version_info >= (3, 9):
    from os import PathLike as _PathProtocol
else:
    _AnyStr_co = TypeVar("_AnyStr_co", str, bytes, covariant=True)

    class _PathProtocol(Protocol[_AnyStr_co]):
        @abstractmethod
        def __fspath__(self) -> _AnyStr_co: ...


# For functions that take a file name
_PathLike = Union[str, bytes, _PathProtocol[str], _PathProtocol[bytes]]
# Most pygame functions that take a file argument should be able to handle a FileLike type
FileLike = Union[_PathLike, IO[bytes], IO[str]]

_T_co = TypeVar("_T_co", covariant=True)


class SequenceLike(Protocol[_T_co]):
    """
    Variant of the standard `Sequence` ABC that only requires `__getitem__` and `__len__`.
    """

    @abstractmethod
    def __getitem__(self, index: int, /) -> _T_co: ...
    @abstractmethod
    def __len__(self) -> int: ...


# Modify typehints when it is possible to annotate sizes

# Pygame handles float without errors in most cases where a coordinate is expected,
# usually rounding to int. Also, 'Union[int, float] == float'
Coordinate = SequenceLike[float]
# This is used where ints are strictly required
IntCoordinate = SequenceLike[int]

ColorLike = Union[int, str, SequenceLike[int]]


class _HasRectAttribute(Protocol):
    # An object that has a rect attribute that is either a rect, or a function
    # that returns a rect conforms to the rect protocol
    @property
    def rect(self) -> Union["RectLike", Callable[[], "RectLike"]]: ...


RectLike = Union[SequenceLike[float], SequenceLike[Coordinate], _HasRectAttribute]


class EventLike(Protocol):
    # __dict__: Dict[str, Any]
    def __init__(
        self, type: int, dict: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> None: ...
    def __new__(cls, *args, **kwargs) -> "EventLike": ...
    def __getattribute__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __int__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __eq__(self, other) -> bool: ...

    @property
    def type(self) -> int: ...
    @property
    def dict(self) -> Dict[str, Any]: ...


# cleanup namespace
del sys, abstractmethod, IO, Callable, Tuple, Union, TypeVar, Protocol
