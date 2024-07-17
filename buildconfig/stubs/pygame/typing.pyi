from typing import IO, Callable, Tuple, Union, TypeVar, Protocol, SupportsIndex

_T1_co = TypeVar("_T1_co", covariant=True)


class _PathProtocol(Protocol[_T1_co]):
    def __fspath__(self) -> _T1_co: ...


PathLike = Union[str, bytes, _PathProtocol[str], _PathProtocol[bytes]]
FileLike = Union[PathLike, IO[bytes], IO[str]]

_T2_co = TypeVar("_T2_co", covariant=True)


class SequenceLike(Protocol[_T2_co]):
    """
    Variant of the standard `Sequence` ABC that only requires `__getitem__` and `__len__`.
    """

    def __getitem__(self, __i: SupportsIndex) -> _T2_co: ...
    def __len__(self) -> int: ...


# Modify typehints when it is possible to annotate sizes
CoordinateLike = SequenceLike[float]
IntCoordinateLike = SequenceLike[int]

RGBALike = Tuple[int, int, int, int]
ColorLike = Union[int, str, SequenceLike[int]]

_CanBeRect = SequenceLike[Union[float, CoordinateLike]]


class _HasRectAttribute(Protocol):
    # An object that has a rect attribute that is either a rect, or a function
    # that returns a rect confirms to the rect protocol
    rect: Union["RectLike", Callable[[], "RectLike"]]


RectLike = Union[_CanBeRect, _HasRectAttribute]
